from starlette import status

from app.exceptions.base import BusinessException


class InvalidInput(BusinessException):
    status: int = status.HTTP_400_BAD_REQUEST
    message: str = "The input provided is invalid."


class UnauthorizedAccess(BusinessException):
    status: int = status.HTTP_401_UNAUTHORIZED
    message: str = "You do not have permission to access this resource."


class InsufficientFunds(BusinessException):
    status: int = status.HTTP_402_PAYMENT_REQUIRED
    message: str = "You have insufficient funds to complete this transaction."


class UserNotFound(BusinessException):
    status: int = status.HTTP_404_NOT_FOUND
    message: str = "User not found in the system."
