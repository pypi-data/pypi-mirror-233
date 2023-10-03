import itertools
from logging import getLogger
from pathlib import Path
import sys
from typing import Iterable


_log = getLogger(__name__)


ROOT_MARKER_FILES = [
    'pyproject.toml',
    'setup.py',
    'requirements.txt',
    'MANIFEST.in',
    '.git',
    '.hg',
]


class ModuleResolveError(ImportError):
    def __str__(self) -> str:
        return f'could not resolve module name for path: {self.path}'


def module_name_from_filename(path: Path, extra_import_paths: Iterable[Path]):
    if path.name == '__init__.py':
        path = path.parent

    modnames = []
    for import_path in itertools.chain(candidate_import_paths(path), extra_import_paths):
        _log.debug(f'import path: {import_path}')
        try:
            relpath = path.relative_to(import_path)
        except ValueError:
            continue

        if not relpath.parts:
            continue

        parts = list(relpath.parts)
        parts[-1] = relpath.stem
        modname = '.'.join(parts)
        _log.debug(f'candidate module name: {modname}')
        modnames.append(modname)

    if not modnames:
        raise ModuleResolveError(path=str(path))

    _, modname = min((len(modname), modname) for modname in modnames)
    _log.debug(f'selected module name: {modname} for path: {str(path)}')
    return modname


def candidate_import_paths(path: Path):
    yield from (Path(path) for path in sys.path)
    project_path = guess_project_path(path)
    if project_path is not None:
        yield project_path


def guess_project_path(path: Path):
    for dir_ in path.parents:
        for marker in ROOT_MARKER_FILES:
            markerpath = dir_.joinpath(marker)
            _log.debug(f'test project marker: { str(markerpath) }')
            if markerpath.exists():
                _log.debug(f'found project: { str(markerpath.parent) }')
                return markerpath.parent

    return None

