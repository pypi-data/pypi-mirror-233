from typing import Any, Optional

from .validation_error_detail import ValidationErrorDetail


class StringTooLongError(ValidationErrorDetail):
    error_type = 'string_too_long'

    def __init__(
        self,
        property: str,
        max_length: int,
        loc: tuple[int | str, ...],
        ctx: Optional[dict[str, dict[str, Any]]] = {},
        input: dict[str, Any] = {},
    ):
        ctx = ctx or {'property': property, 'max_length': max_length}
        super().__init__(self.error_type, loc, '', input, ctx)
