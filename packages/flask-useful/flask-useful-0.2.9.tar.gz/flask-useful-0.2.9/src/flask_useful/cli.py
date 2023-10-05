from __future__ import annotations
import typing as t

import click

if t.TYPE_CHECKING:
    import email_validator
else:
    try:
        import email_validator
    except ImportError:
        email_validator = None


__all__ = (
    'Choice', 'Email',
)


class Choice(click.Choice):
    name = 'extended_choice'

    def __init__(
        self,
        choices: t.Union[
            t.Sequence[t.Any],
            t.Dict[str, t.Any],
            t.Callable[[], t.Sequence[t.Any]]
        ],
        case_sensitive: bool = True,
        field: t.Optional[str] = None,
    ) -> None:
        self._choices = choices
        self.case_sensitive = case_sensitive
        self.field_name = field

    @property
    def choices(self) -> t.Sequence[str]:  # type: ignore
        return tuple(self.choices_map.keys())

    @property
    def choices_map(self) -> t.Dict[str, t.Any]:
        if callable(self._choices):
            self._choices = self._choices()

        if not isinstance(self._choices, dict):
            self._choices = {self.make_key(i): i for i in self._choices}

        return self._choices

    def convert(
        self,
        value: t.Any,
        param: t.Optional[click.Parameter],
        ctx: t.Optional[click.Context],
    ) -> t.Any:
        if value in self.choices_map.values():
            return value
        result = super().convert(value, param, ctx)
        return self.choices_map[result]

    def get_missing_message(self, param: click.Parameter) -> str:
        try:
            return super().get_missing_message(param)
        except RuntimeError:
            return ''

    def make_key(self, value: t.Any) -> str:
        if self.field_name is None:
            return str(value)
        elif isinstance(value, dict):
            return str(value[self.field_name])
        else:
            return str(getattr(value, self.field_name))


class Email(click.ParamType):
    name = 'email'

    def __init__(self, **options: t.Any) -> None:
        self.options = options

    def convert(
        self,
        value: str,
        param: t.Optional[click.Parameter],
        ctx: t.Optional[click.Context],
    ) -> str:
        if email_validator is None:
            raise RuntimeError('The email-validator package must be installed.')

        try:
            email_validator.validate_email(value, **self.options)
        except email_validator.EmailNotValidError as err:
            self.fail(str(err), param, ctx)

        return value
