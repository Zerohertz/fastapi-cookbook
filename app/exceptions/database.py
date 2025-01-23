from starlette import status

from app.exceptions.base import CoreException


class DatabaseException(CoreException):
    status: int
    message: str


class EntityNotFound(DatabaseException):
    status: int = status.HTTP_404_NOT_FOUND
    message: str = "Entity not found in the database."
