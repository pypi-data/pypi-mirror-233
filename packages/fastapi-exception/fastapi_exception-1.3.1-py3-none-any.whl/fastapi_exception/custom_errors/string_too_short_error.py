from typing import Any, Optional

from .validation_error_detail import ValidationErrorDetail


class StringTooShortError(ValidationErrorDetail):
    error_type = 'string_too_short'
    msg_template = '%{property} should have at least %{min_length} characters'

    def __init__(
        self,
        property: str,
        min_length: int,
        loc: tuple[int | str, ...],
        ctx: Optional[dict[str, dict[str, Any]]] = {},
        input: dict[str, Any] = {},
    ):
        ctx = ctx or {'property': property, 'min_length': min_length}
        msg = self.msg_template.format(property=property, min_length=min_length)
        super().__init__(self.error_type, loc, msg, input, ctx)
