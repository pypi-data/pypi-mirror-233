from typing import Any, Optional, TypedDict


class ValidationErrorDetail(TypedDict):
    type: str
    loc: tuple[int | str, ...]
    msg: str
    custom_msg: Optional[str]
    input: dict[str, Any]
    ctx: Optional[dict[str, dict[str, Any]]]
