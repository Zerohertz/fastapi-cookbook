from typing import Annotated, Sequence

from pydantic import EmailStr, StringConstraints

from app.models.enums import Role
from app.schemas.auth import AuthOut, AuthResponse
from app.schemas.base import BaseRequest, BaseResponse


class UserRequest(BaseRequest):
    name: Annotated[str, StringConstraints(min_length=3, max_length=30)]


class UserPatchRequest(BaseRequest):
    name: Annotated[str | None, StringConstraints(min_length=3, max_length=30)] = None
    password: Annotated[str | None, StringConstraints(min_length=3, max_length=30)] = (
        None
    )


class UserResponse(BaseResponse):
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
