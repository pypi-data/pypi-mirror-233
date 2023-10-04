from typing import Any, Optional

from .validation_error_detail import ValidationErrorDetail


class StringTooShortError(ValidationErrorDetail):
    error_type = 'string_too_short'
    msg = 'Field should have at least {min_length} characters'
    msg_template = '{property} should have at least {min_length} characters'

    def __init__(
        self,
        min_length: int,
        loc: tuple[int | str, ...],
        ctx: Optional[dict[str, dict[str, Any]]] = {},
        property: Optional[str] = None,
        input: dict[str, Any] = {},
        custom_msg: Optional[str] = '',
    ):
        msg = self.msg.format(min_length=min_length)
        ctx = ctx or {'property': property or loc[-1], 'min_length': min_length}
        super().__init__(self.error_type, loc, msg, input, ctx, property, custom_msg)
