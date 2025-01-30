from fastapi import status

from app.exceptions.base import CoreException


class DatabaseException(CoreException):
    status: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Database error occurred."


class EntityAlreadyExists(DatabaseException):
    status: int = status.HTTP_409_CONFLICT
    message: str = "Entity already exists in the database."


class EntityNotFound(DatabaseException):
    status: int = status.HTTP_404_NOT_FOUND
    message: str = "Entity not found in the database."
