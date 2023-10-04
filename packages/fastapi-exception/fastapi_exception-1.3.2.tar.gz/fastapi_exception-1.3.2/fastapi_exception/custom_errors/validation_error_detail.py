from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ValidationErrorDetail:
    type: str
    """
    The type of error that occurred, this is an identifier designed for
    programmatic use that will change rarely or never.

    `type` is unique for each error message, and can hence be used as an identifier to build custom error messages.
    """
    loc: tuple[int | str, ...]
    """Tuple of strings and ints identifying where in the schema the error occurred."""
    msg: str
    """A human readable error message."""
    input: dict[str, Any]
    """The input data at this `loc` that caused the error."""
    ctx: Optional[dict[str, dict[str, Any]]]
    """
    Values which are required to render the error message, and could hence be useful in rendering custom error messages.
    Also useful for passing custom error data forward.
    """
    custom_msg: Optional[str] = ''

    property: Optional[str] = None
    """
    No need to add key, value in validation.json file to translate error message
    """
