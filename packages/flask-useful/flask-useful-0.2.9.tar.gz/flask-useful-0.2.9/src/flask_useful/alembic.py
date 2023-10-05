from __future__ import annotations
import typing as t

from alembic.operations import Operations, MigrateOperation
from sqlalchemy_utils.view import CreateView, DropView

if t.TYPE_CHECKING:
    from sqlalchemy import Select


@Operations.register_operation('create_view')
class CreateViewOp(MigrateOperation):
    """Create a VIEW."""

    def __init__(
        self,
        view_name: str,
        selectable: Select[t.Any],
        materialized: bool = False,
        schema: t.Optional[str] = None,
    ) -> None:
        self.view_name = view_name
        self.selectable = selectable
        self.materialized = materialized
        self.schema = schema

    @classmethod
    def create_view(
        cls,
        operations: Operations,
        view_name: str,
        selectable: Select[t.Any],
        materialized: bool = False,
        **kw: t.Any,
    ) -> None:
        """Issue a "CREATE VIEW" instruction."""
        op = cls(view_name, selectable, materialized, **kw)
        operations.invoke(op)

    def reverse(self) -> DropViewOp:
        # only needed to support autogenerate
        return DropViewOp(self.view_name, schema=self.schema)


@Operations.register_operation('drop_view')
class DropViewOp(MigrateOperation):
    """Drop a VIEW."""

    def __init__(
        self,
        view_name: str,
        materialized: bool = False,
        cascade: bool = True,
        schema: t.Optional[str] = None,
    ) -> None:
        self.view_name = view_name
        self.materialized = materialized
        self.cascade = cascade
        self.schema = schema

    @classmethod
    def drop_view(
        cls,
        operations: Operations,
        view_name: str,
        materialized: bool = False,
        cascade: bool = True,
        **kw: t.Any,
    ) -> None:
        """Issue a "DROP VIEW" instruction."""
        op = cls(view_name, materialized, cascade, **kw)
        operations.invoke(op)


@Operations.implementation_for(CreateViewOp)
def create_view(operations: Operations, operation: CreateViewOp) -> None:
    if operation.schema is not None:
        name = '%s.%s' % (operation.schema, operation.view_name)
    else:
        name = operation.view_name
    operations.execute(CreateView(name, operation.selectable))


@Operations.implementation_for(DropViewOp)
def drop_view(operations: Operations, operation: DropViewOp) -> None:
    if operation.schema is not None:
        name = '%s.%s' % (operation.schema, operation.view_name)
    else:
        name = operation.view_name
    operations.execute(DropView(name))
