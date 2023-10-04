from typing import List, Union

from fastapi import FastAPI
from fastapi_global_variable import GlobalVariable
from pydantic import BaseModel, Field

from fastapi_exception import (DuplicateError, FastApiException, MissingError, StringTooLongError, throw_validation,
                               throw_validation_with_exception)

from .config.i18n import i18n_service

app = FastAPI(title="Test App")

GlobalVariable.set('app', app)

FastApiException.config(i18n_service)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None
    x: List[int] = Field(min_length=3)
    y: List[int] = Field(max_length=1)


@app.post("/items")
def create_items(item: Item):
    return {"item_name": item.name}


@app.post("/cars")
def create_cars():
    # throw_validation(type='invalid_car_wheel', loc=('body', 'wheel'))
    # throw_validation_with_exception(DuplicateError(loc=('body', 'wheel')))
    throw_validation_with_exception(StringTooLongError(max_length=1, loc=('body', 'wheel')))
    # throw_validation_with_exception(MissingError(loc=('body', 'wheel')))
    return True
