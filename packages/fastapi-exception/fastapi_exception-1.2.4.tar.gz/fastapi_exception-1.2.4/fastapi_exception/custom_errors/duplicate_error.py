from typing import Any, Optional

from .validation_error_detail import ValidationErrorDetail


class DuplicateError(ValidationErrorDetail):
    error_type = 'duplicate'
    msg_template = '{property} is already in used'

    def __init__(
        self,
        property: str,
        loc: tuple[int | str, ...],
        ctx: Optional[dict[str, dict[str, Any]]] = {},
        input: dict[str, Any] = {},
    ):
        msg = self.msg_template.format(property=property)
        super().__init__(self.error_type, loc, msg, input, ctx, custom_msg=msg)
