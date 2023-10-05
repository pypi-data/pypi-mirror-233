"""
The module contains functions for automating the configuration of the application object.
"""

from __future__ import annotations
from contextlib import suppress
import json
import os
import pathlib
import typing as t

from flask import Blueprint, Flask
from flask.cli import AppGroup
from werkzeug.utils import find_modules, import_string


__all__ = (
    'config_from_prefixed_env',
    'config_from_secrets_env',
    'register_blueprints',
    'register_commands',
    'register_extensions',
)


AppOrBp = t.Union[Flask, Blueprint]


def config_from_prefixed_env(
    app: Flask, prefix: str = 'FLASK', *, loads: t.Callable[[str], t.Any] = json.loads,
) -> bool:
    """
    For backward compatibility with Flask < 2.1.
    Documentation: https://flask.palletsprojects.com/en/2.3.x/api/
    """
    if hasattr(app.config, 'from_prefixed_env'):
        return app.config.from_prefixed_env(prefix, loads=loads)

    prefix = '%s_' % prefix
    prefix_len = len(prefix)

    for key in filter(lambda k: k.startswith(prefix), os.environ):
        value = os.environ[key]

        with suppress(Exception):
            value = loads(value)

        key = key[prefix_len:]
        current = app.config
        *parent_keys, key = key.split('__')

        for parent in parent_keys:
            current.setdefault(parent, {})
            current = current[parent]

        current[key] = value

    return True


def config_from_secrets_env(app: Flask, prefix: str = 'SECRET') -> None:
    """
    Loads configuration parameter values from Docker secrets.

    Paths to secret files are passed through any environment variables
    that start with SECRET_,
    dropping the prefix from the env key for the config key.
    """
    def loads(path: str) -> t.Any:
        path, *key = path.rsplit('|', maxsplit=1)
        value = pathlib.Path(path).read_text()

        if not key:
            return value

        return json.loads(value).__getitem__(key[0])

    config_from_prefixed_env(app=app, prefix=prefix, loads=loads)


def get_import_prefix(app: AppOrBp) -> str:
    if app.import_name == '__main__':
        return ''
    return f'{app.import_name}.'


def get_import_path(app: AppOrBp, import_path: str) -> str:
    """Returns the absolute path to import a module or package."""
    prefix = get_import_prefix(app)
    return (prefix + import_path).strip('.')


def register_blueprints(
    app: AppOrBp,
    import_path: str,
    recursive: bool = False,
    include_packages: bool = False,
) -> None:
    """
    Registers Blueprint for the specified application.

    The argument `import_path` must be a valid import name for the package that contains the modules.
    One module - one Blueprint.
    The variable named `bp` must contain an instance of Blueprint.

    If the `BLUEPRINT_DISABLED` attribute is set in the module, then Blueprint will be ignored.
    """
    modules_names = list(find_modules(
        get_import_path(app, import_path),
        recursive=recursive,
        include_packages=include_packages,
    ))

    for name in modules_names:
        mod = import_string(name)

        if hasattr(mod, 'bp') and not getattr(mod.bp, 'BLUEPRINT_DISABLED', False):
            if isinstance(mod.bp, Blueprint):
                app.register_blueprint(mod.bp)


def register_commands(app: Flask, import_name: str) -> None:
    """Initializes console commands found at the specified import path.

    If the __all__ attribute is specified in the module,
    it will be used to fund commands.
    Otherwise, the search is performed using the `dir` function.

    Command is an object inherited from `flask.cli.AppGroup`.
    """
    m = import_string(get_import_path(app, import_name))

    for name in getattr(m, '__all__', dir(m)):
        prop = getattr(m, name)

        if isinstance(prop, AppGroup):
            app.cli.add_command(prop)


def register_extensions(app: Flask, import_name: str) -> None:
    """Initializes all Flask extensions found in the specified import path.

    If the __all__ attribute is specified in the module,
    it will be used to search for extension instances.
    Otherwise, the search is performed using the `dir` function.

    An extension is an object that has an init_app method.
    """
    m = import_string(get_import_path(app, import_name))

    for name in getattr(m, '__all__', dir(m)):
        prop = getattr(m, name)
        init_app = getattr(prop, 'init_app', None)

        if callable(init_app):
            init_app(app)
