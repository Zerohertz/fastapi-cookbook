from typing import Optional

from pydantic import EmailStr, constr

from app.models.enums import Role
from app.schemas.auth import AuthOut, AuthResponse
from app.schemas.base import BaseRequest, BaseResponse


class UserRequest(BaseRequest):
    name: constr(min_length=3, max_length=30)


class UserPatchRequest(BaseRequest):
    name: Optional[constr(min_length=3, max_length=30)] = None
    password: Optional[constr(min_length=8, max_length=30)] = None


class UserResponse(BaseResponse):
    name: constr(min_length=3, max_length=30)
    email: EmailStr
    role: Role
    oauth: list[AuthResponse] = []


class UserIn(UserRequest):
    email: EmailStr
    role: Role
    refresh_token: Optional[str] = None


class UserOut(UserResponse):
    refresh_token: Optional[str] = None
    oauth: list[AuthOut] = []
