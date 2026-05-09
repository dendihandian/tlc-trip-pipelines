from typing import Annotated
from typer import run, Argument, Option, BadParameter

VALIDATION_ERROR_DATE = 'invalid date format'

def validate_parameter(value, validator, message = ''):
    if validator(value) is False:
        raise BadParameter(message)
    return value