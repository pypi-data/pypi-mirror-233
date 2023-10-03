import ast
import inspect


def capture_last_expression(mod: ast.Module, target: str):
    if len(mod.body) > 0 and isinstance(mod.body[-1], ast.Expr):
        mod.body[-1] = ast.Assign(
            targets=[ast.Name(target, ast.Store())],
            value=mod.body[-1].value,
        )
        ast.fix_missing_locations(mod)


if hasattr(ast, 'PyCF_ALLOW_TOP_LEVEL_AWAIT'):
    async def aexec(code, filename, globals=..., locals=...):
        code_object = compile(code, filename, 'exec', ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
        if code_object.co_flags & inspect.CO_COROUTINE:
            await eval(code_object, globals, locals)
        else:
            exec(code_object, globals, locals)
else:
    import aeval
    async def aexec(code, filename, globals=..., locals=...):
        # TODO: Use filename.
        await aeval.aeval(code, globals, locals)
