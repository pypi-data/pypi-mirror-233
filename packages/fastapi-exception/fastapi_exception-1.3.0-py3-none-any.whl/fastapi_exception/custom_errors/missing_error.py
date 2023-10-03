from typing import Any, Optional

from .validation_error_detail import ValidationErrorDetail


class MissingError(ValidationErrorDetail):
    error_type = 'missing'

    def __init__(
        self,
        property: str,
        loc: tuple[int | str, ...],
        ctx: Optional[dict[str, dict[str, Any]]] = {},
        input: dict[str, Any] = {},
    ):
        ctx = ctx or {'property': property}
        super().__init__(self.error_type, loc, '', input, ctx)
