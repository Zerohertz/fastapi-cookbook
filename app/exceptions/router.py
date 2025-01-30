from fastapi import status

from app.exceptions.base import CoreException


class RouterException(CoreException):
    status: int
    message: str


class RouterTypeError(RouterException):
    status: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Invalid router return type."
