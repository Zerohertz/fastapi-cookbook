from starlette import status

from app.exceptions.base import CoreException


class EntityNotFound(CoreException):
    status: int = status.HTTP_404_NOT_FOUND
    message: str = "Entity not found in the database."
