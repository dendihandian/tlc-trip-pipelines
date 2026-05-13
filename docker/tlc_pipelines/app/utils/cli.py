from typing import Annotated
from typer import run, Argument, Option, BadParameter

VALIDATION_ERROR_DATE = 'invalid date format'
VALIDATION_ERROR_CASE = 'value not recognized'

def validate_parameter(value, validator, message = ''):
    if validator(value) is False:
        raise BadParameter(message)
    return value