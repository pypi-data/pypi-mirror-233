from typing import Any, Optional

from .validation_error_detail import ValidationErrorDetail


class DuplicateError(ValidationErrorDetail):
    error_type = 'duplicate'
    msg = 'Field is already in used'

    def __init__(
        self,
        loc: tuple[int | str, ...],
        ctx: Optional[dict[str, dict[str, Any]]] = {},
        property: Optional[str] = None,
        input: dict[str, Any] = {},
        custom_msg: Optional[str] = '',
    ):
        super().__init__(self.error_type, loc, self.msg, input, ctx, custom_msg, property)
