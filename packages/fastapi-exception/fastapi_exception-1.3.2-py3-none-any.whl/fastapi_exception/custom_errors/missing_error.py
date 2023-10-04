from typing import Any, Optional

from .validation_error_detail import ValidationErrorDetail


class MissingError(ValidationErrorDetail):
    error_type = 'missing'
    msg = 'Field is required'

    def __init__(
        self,
        loc: tuple[int | str, ...],
        property: Optional[str] = None,
        ctx: Optional[dict[str, dict[str, Any]]] = {},
        input: dict[str, Any] = {},
        custom_msg: Optional[str] = '',
    ):
        super().__init__(self.error_type, loc, self.msg, input, ctx, custom_msg, property)
