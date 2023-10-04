from typing import Any, Optional

from .validation_error_detail import ValidationErrorDetail


class StringTooLongError(ValidationErrorDetail):
    error_type = 'string_too_long'
    msg = 'Field should have at most {max_length} characters'
    msg_template = '{property} should have at most {max_length} characters'

    def __init__(
        self,
        max_length: int,
        loc: tuple[int | str, ...],
        ctx: Optional[dict[str, dict[str, Any]]] = {},
        property: Optional[str] = None,
        input: dict[str, Any] = {},
        custom_msg: Optional[str] = '',
    ):
        msg = self.msg.format(max_length=max_length)
        ctx = ctx or {'property': property or loc[-1], 'max_length': max_length}
        super().__init__(self.error_type, loc, msg, input, ctx, custom_msg, property)
