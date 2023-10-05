from __future__ import annotations
import typing as t
from urllib.parse import urlparse

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

from .confirmation_token import *
from .session import *
from .utils import *

if t.TYPE_CHECKING:
    from flask import Flask


__all__ = (
    'generate_slug',
    'get_primary_columns',
    'get_sqla_session',
    'normalize_pk',
    'sqla_session',
    'ConfirmationToken',
    'ConfirmationTokenSerializer',
    'SQLAlchemy',
)


class SQLAlchemy(_SQLAlchemy):
    def init_app(self, app: Flask) -> None:
        def prepare_url(url: str, prefix: str = '') -> str:
            if url.startswith('sqlite'):
                return url

            prefix = f'SQLALCHEMY_{prefix}'.strip('_').upper()
            dsn = urlparse(url)

            user = app.config.get(f'{prefix}_USER', dsn.username)
            password = app.config.get(f'{prefix}_PASSWORD', dsn.password)
            host = app.config.get(f'{prefix}_HOST', dsn.hostname)
            port = app.config.get(f'{prefix}_PORT', dsn.port)

            auth = user if password is None else '%s:%s' % (user, password)
            addr = host if port is None else '%s:%s' % (host, port)
            netloc = '%s@%s' % (auth, addr) if auth else addr

            return dsn._replace(
                netloc=netloc,
                path=app.config.get(f'{prefix}_DATABASE', dsn.path)
            ).geturl()

        if 'SQLALCHEMY_DATABASE_URI' in app.config:
            app.config['SQLALCHEMY_DATABASE_URI'] = prepare_url(
                app.config['SQLALCHEMY_DATABASE_URI']
            )

        if 'SQLALCHEMY_BINDS' in app.config:
            binds = {
                name: {'url': cnf} if isinstance(cnf, str) else cnf
                for name, cnf in app.config['SQLALCHEMY_BINDS'].items()
            }

            for name, params in binds.items():
                params['url'] = prepare_url(params['url'], prefix=name)

            app.config['SQLALCHEMY_BINDS'] = binds

        super().init_app(app)
