from typing import Optional

from pydantic import EmailStr, constr

from app.models.enums import OAuthProvider, Role
from app.schemas.base import BaseRequest, BaseResponse


class UserRequest(BaseRequest):
    name: constr(min_length=3, max_length=30)
    email: EmailStr


class UserPatchRequest(BaseRequest):
    name: Optional[constr(min_length=3, max_length=30)] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=8, max_length=30)] = None


class UserResponse(BaseResponse):
    name: constr(min_length=3, max_length=30)
    email: EmailStr
    oauth: OAuthProvider


class UserIn(UserRequest):
    role: Role
    oauth: OAuthProvider
    password: Optional[constr(min_length=8, max_length=30)] = None
    refresh_token: Optional[str] = None
    oauth_token: Optional[str] = None


class UserOut(UserResponse):
    role: Role
    password: Optional[str] = None
    refresh_token: Optional[str] = None
    oauth_token: Optional[str] = None
