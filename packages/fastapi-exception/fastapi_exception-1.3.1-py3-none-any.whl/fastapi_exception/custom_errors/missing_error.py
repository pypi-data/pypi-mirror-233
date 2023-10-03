from typing import Any, Optional

from .validation_error_detail import ValidationErrorDetail


class MissingError(ValidationErrorDetail):
    error_type = 'missing'
    msg_template = '{property} is required'

    def __init__(
        self,
        property: str,
        loc: tuple[int | str, ...],
        ctx: Optional[dict[str, dict[str, Any]]] = {},
        input: dict[str, Any] = {},
    ):
        ctx = ctx or {'property': property}
        msg = self.msg_template.format(property=property)
        super().__init__(self.error_type, loc, msg, input, ctx)
