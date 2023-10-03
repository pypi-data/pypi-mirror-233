#!/usr/bin/env python3
'''
Functions for dynamically importing modules.
'''

import logging
import pathlib
import pkgutil


LOGGER = logging.getLogger(__name__)


def import_modules(paths, path_log_msg=None):
    '''
    Import modules by paths.

    Args:
        paths:
            An iterable of file and directory paths. File paths will import
            single modules while directory paths will recursively import all
            modules contained in the directory.

        path_log_msg:
            An optional logging format string for logging messages about the
            given paths. If given, it should contain a single "%s" placeholder
            for the path argument.

    Returns:
        The set of loaded module names.
    '''
    paths = set(pathlib.Path(path).resolve() for path in paths)
    if not paths:
        LOGGER.warning('No paths passed to import_modules().')

    if path_log_msg:
        for path in sorted(paths):
            LOGGER.debug(path_log_msg, path)

    file_paths = set()
    dir_paths = set()
    for path in paths:
        if path.is_dir():
            dir_paths.add(path)
        else:
            file_paths.add(path)

    all_dir_paths = sorted(dir_paths | set(path.parent for path in file_paths))

    loaded = set()
    for loader, name, _is_pkg in pkgutil.walk_packages(path=all_dir_paths):
        path = pathlib.Path(loader.path) / f'{name}.py'
        if path in file_paths or any(path.is_relative_to(p) for p in dir_paths):
            LOGGER.debug('Loading module %s from %s', name, path)
            loader.find_module(name).load_module(name)
            loaded.add(name)

    return loaded
