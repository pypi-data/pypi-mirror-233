from __future__ import annotations
from contextlib import contextmanager
import typing as t

from flask import current_app
from sqlalchemy.orm import Session
from werkzeug.local import LocalProxy


__all__ = (
    'get_sqla_session',
    'sqla_session',
)


class SupportsAutocommit(t.Protocol):
    @contextmanager
    def autocommit(self) -> t.Iterator[Session]: ...


class SessionProxyType(Session, SupportsAutocommit):
    ...


def get_sqla_session() -> Session:
    """Returns the current session instance from application context."""
    ext = current_app.extensions.get('sqlalchemy')

    if ext is None:
        raise RuntimeError(
            'An extension named sqlalchemy was not found '
            'in the list of registered extensions for the current application.'
        )

    return t.cast(Session, ext.db.session)


class SessionProxy(LocalProxy[Session]):
    def __init__(self) -> None:
        super().__init__(lambda: get_sqla_session())

    @contextmanager
    def autocommit(self, rollback: bool = False) -> t.Iterator[Session]:
        """
        Returns the current session as the value of the context manager.

        If successful, commits the changes.
        """
        try:
            yield self._get_current_object()
            self._get_current_object().commit()
            rollback = False
        finally:
            if rollback:
                self._get_current_object().rollback()


sqla_session = t.cast(SessionProxyType, SessionProxy())
