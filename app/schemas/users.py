from typing import Annotated, Sequence

from pydantic import EmailStr, StringConstraints

from app.models.enums import Role
from app.schemas.auth import AuthOut, AuthResponse
from app.schemas.base import BaseDBResponse, BaseRequest


class UserRequest(BaseRequest):
    name: Annotated[str, StringConstraints(min_length=3, max_length=30)]


class UserPasswordRequest(BaseRequest):
    password_old: Annotated[str, StringConstraints(min_length=8, max_length=30)]
    password_new: Annotated[str, StringConstraints(min_length=8, max_length=30)]


class UserPasswordAdminRequest(BaseRequest):
    password: Annotated[str, StringConstraints(min_length=8, max_length=30)]


class UserResponse(BaseDBResponse):
    name: Annotated[str, StringConstraints(min_length=3, max_length=30)]
    email: EmailStr
    role: Role
    oauth: Sequence[AuthResponse] = []


class UserIn(UserRequest):
    email: EmailStr
    role: Role
    refresh_token: str | None = None


class UserOut(UserResponse):
    refresh_token: str | None = None
    oauth: Sequence[AuthOut] = []
