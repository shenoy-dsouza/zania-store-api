from store.exceptions import BaseException
from store.error_codes import VALIDATION_ERROR
from rest_framework import status


class InsufficientStockException(BaseException):
    http_status_code = status.HTTP_400_BAD_REQUEST
    error_code = VALIDATION_ERROR
    message = "Insufficient stock"
