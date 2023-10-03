import argparse
import ast
import functools
import importlib
import inspect
from logging import getLogger
import os
from pathlib import Path
from textwrap import dedent
import traceback
import sys
import types
from typing import Awaitable, Callable, Dict, Union

import lsp
import trio

from .evaluation import capture_last_expression, aexec
from .resolution import ModuleResolveError, module_name_from_filename


_log = getLogger(__name__)


def main():
    import logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    _log.addHandler(ch)
    _log.setLevel(logging.INFO)

    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('-H', '--host', default=None)
    parser.add_argument('-p', '--port', default=6768, type=int)
    parser.add_argument('-f', '--portfile', default='./.lyre-port')
    args = parser.parse_args()

    sys.path.insert(0, '.')

    trio.run(functools.partial(
        run,
        host=args.host,
        port=args.port,
        portfile=args.portfile,
    ))


async def run(host=None, port=6768, portfile='./.lyre-port'):
    listeners = await trio.open_tcp_listeners(port, host=host)
    if portfile:
        with open(portfile, 'w') as f:
            for listener in listeners:
                host, port, *_ = listener.socket.getsockname()
                f.write(f'{host} {port}\n')
    try:
        await trio.serve_listeners(_handler, listeners)
    finally:
        if portfile:
            os.remove(portfile)


class Shutdown(Exception):
    ...


Context = Dict
Request = Dict
Result = Dict
Handler = Callable[[Context, Request], Union[Result, Awaitable[Result]]]


async def _handler(stream: trio.SocketStream):
    _log.info('connected')
    conn = lsp.Connection('server')
    recvsize = 4096
    ctx: Context = dict()

    handlers: Dict[str, Handler] = {
        "initialize": _initialize,
        "shutdown": _shutdown,
        "lyre/eval": _eval,
    }

    try:
        while True:
            while True:
                event = conn.next_event()

                if event is lsp.NEED_DATA:
                    data = await stream.receive_some(recvsize)
                    if not data:
                        return
                    conn.receive(data)
                elif isinstance(event, lsp.RequestReceived):
                    ...
                elif isinstance(event, lsp.DataReceived):
                    ...
                elif isinstance(event, lsp.MessageEnd):
                    break

            _, body = conn.get_received_data()

            if "id" in body:
                await _handle_request(stream, conn, handlers, ctx, body)
            else:
                # TODO: Handle notifications
                ...

            conn.go_next_circle()
    except Shutdown:
        ...
    finally:
        _log.info('disconnected')


async def _handle_request(
    stream: trio.SocketStream,
    conn: lsp.Connection,
    handlers: Dict[str, Handler],
    ctx: Context,
    request: Request,
):
    method = request.get("method", None)
    _log.debug(f"handling request: {method}")
    _log.debug(request)

    handler = handlers.get(method, _not_found)

    response = dict(id=request["id"])
    try:
        result = handler(ctx, request)
        if inspect.isawaitable(result):
            result = await result
        response["result"] = result
    except BaseException:
        response["result"] = _error_result()

    send_data = conn.send_json(response)
    await stream.send_all(send_data)


def _initialize(ctx: Context, request: Request) -> Result:
    ctx.clear()
    return dict(capabilities=dict())


def _shutdown(ctx: Context, request: Request) -> Result:
    ctx.clear()
    raise Shutdown()


def _not_found(ctx: Context, request: Request) -> Result:
    ...


async def _eval(ctx: Context, request: Request) -> Result:
    try:
        params = request['params']
        path = Path(params['path'])
        import_paths = [Path(x) for x in params.get("importPaths", [])]
        code = params['code']
        lineno = params.get('lineno', 1)
    except KeyError:
        # TODO: More precise error result.
        raise

    try:
        modname = module_name_from_filename(path, import_paths)
    except ModuleResolveError:
        # TODO: More precise error result.
        raise

    try:
        mod = importlib.import_module(modname)
    except Exception:
        print(f'import failed: {modname}')
        mod = sys.modules[modname] = types.ModuleType(
            modname, 'Synthetic module created by Lyre')
        mod.__file__ = str(path)

    # TODO: Would be nice to source map back to the indented version for
    #       SyntaxError exceptions, especially.
    code = dedent(code)

    try:
        node = ast.parse(code, str(path), 'exec')
        ast.increment_lineno(node, lineno - 1)
        capture_last_expression(node, '--lyre-result--')

        await aexec(node, str(path), mod.__dict__, mod.__dict__)
        value = mod.__dict__.pop('--lyre-result--', None)
        return dict(status='ok', value=repr(value))
    finally:
        mod.__dict__.pop('--lyre-result--', None)


def _error_result():
    etype, ex, tb = sys.exc_info()
    fmt_exc = traceback.format_exception_only(etype, ex)
    fmt_tb = traceback.format_tb(tb)

    return dict(
        status='error',
        error=fmt_exc[-1],
        fullError=fmt_exc,
        traceback=fmt_tb,
    )
