from typing import Any, Optional, Tuple, Union

from fastapi.exceptions import RequestValidationError
from pydantic_core import ErrorDetails

from fastapi_exception.custom_errors.validation_error_detail import ValidationErrorDetail


def throw_validation(
    type: str,
    loc: Union[str, Tuple[Union[int, str], ...]] = (),
    input: Optional[dict[Any, str]] = {},
    ctx: Optional[dict[str, Any]] = {},
):
    raise RequestValidationError([ErrorDetails(loc=loc, type=type, input=input, ctx=ctx)])


def throw_validation_with_exception(exception: ValidationErrorDetail):
    raise RequestValidationError([exception])
