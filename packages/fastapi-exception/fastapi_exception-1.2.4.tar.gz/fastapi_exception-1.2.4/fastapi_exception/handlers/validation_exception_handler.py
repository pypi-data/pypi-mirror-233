from typing import Any, Optional, Tuple, Union

from fastapi_global_variable import GlobalVariable
from pydantic import ValidationError
from requests import Request
from starlette import status
from starlette.responses import JSONResponse

from fastapi_exception.custom_errors.validation_error_detail import ValidationErrorDetail

from ..translators.base_translator_service import BaseTranslatorService


class ErrorResponse:
    def __init__(self, translator_service: BaseTranslatorService, error: ValidationErrorDetail):
        self.translator_service = translator_service
        self.loc = error.get('loc')
        self.type = error.get('type')
        self.ctx = error.get('ctx')
        self.custom_msg = error.get('custom_msg')

    def build_constrains(self, loc: Tuple[Union[int, str], ...], ctx: Optional[dict[str, Any]]):
        constraints = {'property': loc[-1]}

        if ctx:
            constraints.update(ctx)

        return constraints

    def translate_message(self):
        constraints = self.build_constrains(self.loc, self.ctx)
        return self.translator_service.translate(f'validation.{self.type}', **constraints)

    def generate(self):
        return {'type': self.type, 'loc': self.loc, 'msg': self.custom_msg or self.translate_message()}


async def validation_exception_handler(request: Request, error: ValidationError):  # pylint: disable=unused-argument
    response = {'message': 'Validation error', 'errors': translate_errors(error.errors())}
    return JSONResponse(response, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def translate_errors(errors: list[ValidationErrorDetail]) -> list[ValidationErrorDetail]:
    translator_service: BaseTranslatorService = GlobalVariable.get('translator_service')

    if not translator_service:
        return errors

    return [ErrorResponse(translator_service, error).generate() for error in errors]
