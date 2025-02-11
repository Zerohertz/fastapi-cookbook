from fastapi import status

from app.exceptions.base import CoreException


class AuthException(CoreException): ...


class UserAlreadyExists(AuthException):
    status: int = status.HTTP_409_CONFLICT
    message: str = "User already exists. Please use a different email."


class NotRegistered(AuthException):
    status: int = status.HTTP_404_NOT_FOUND
    message: str = "User not registered. Please sign up first."


class OAuthFormDataInvalid(AuthException):
    status: int = status.HTTP_400_BAD_REQUEST
    message: str = "Invalid form data or missing fields in OAuth request."


class PasswordOAuthFailed(AuthException):
    status: int = status.HTTP_401_UNAUTHORIZED
    message: str = "Invalid username or password."


class GoogleOAuthFailed(AuthException):
    status: int = status.HTTP_400_BAD_REQUEST
    message: str = "Google OAuth authentication failed."


class GitHubOAuthFailed(AuthException):
    status: int = status.HTTP_400_BAD_REQUEST
    message: str = "GitHub OAuth authentication failed."


class NotAuthenticated(CoreException):
    status: int = status.HTTP_403_FORBIDDEN
    message: str = "Authentication required. Please log in."


class TokenDecodeError(AuthException):
    status: int = status.HTTP_400_BAD_REQUEST
    message: str = "Token decode error."


class TokenExpired(AuthException):
    status: int = status.HTTP_401_UNAUTHORIZED
    message: str = "Expired token."
