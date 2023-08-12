"""
Handled exceptions raised CustomValidationError.
"""

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    response = exception_handler(exc, context)
    handlers = {
        'ProfileDoesNotExist': _handle_generic_error,
        'ValidationError': _handle_generic_error
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    response.data = {
        'success': False,
        'message': 'Validation error',
        'errors': response.data
    }

    return response


class CustomValidationError(APIException):
    default_detail = _('Validation error')  # or Invalid input
    default_message = _('Not found')

    def __init__(self, msg: str = default_detail, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.status_code = status_code
        self.detail = {'success': False, 'message': msg}


