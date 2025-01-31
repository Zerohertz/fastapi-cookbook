from fastapi import status

from app.exceptions.base import CoreException


class RouterException(CoreException): ...


class RouterTypeError(RouterException):
    status: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Invalid router return type."
