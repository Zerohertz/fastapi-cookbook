from fastapi import status

from app.exceptions.base import CoreException


class AuthException(CoreException):
    status: int
    message: str


class UserAlreadyExists(CoreException):
    status: int = status.HTTP_409_CONFLICT
    message: str = "User already exists. Please use a different email."


class NotRegistered(CoreException):
    status: int = status.HTTP_404_NOT_FOUND
    message: str = "User not registered. Please sign up first."


class LoginFailed(CoreException):
    status: int = status.HTTP_401_UNAUTHORIZED
    message: str = "Login failed. Invalid credentials."


class GitHubOAuth(AuthException):
    status: int = status.HTTP_400_BAD_REQUEST
    message: str = "GitHub OAuth failed."


class NotAuthenticated(CoreException):
    status: int = status.HTTP_403_FORBIDDEN
    message: str = "Not authenticated."


class TokenDecode(AuthException):
    status: int = status.HTTP_400_BAD_REQUEST
    message: str = "Token decode error."


class TokenExpired(AuthException):
    status: int = status.HTTP_400_BAD_REQUEST
    message: str = "Expired token."
