from typing import Optional

from app.models.enums import OAuthProvider, Role
from app.schemas.base import BaseRequest, BaseResponse


class UserRequest(BaseRequest):
    name: str
    # TODO: Email 검증
    email: str


class UserPatchRequest(BaseRequest):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserResponse(BaseResponse):
    name: str
    email: str
    oauth: OAuthProvider


class UserIn(UserRequest):
    role: Role
    oauth: OAuthProvider
    password: Optional[str] = None
    refresh_token: Optional[str] = None
    github_token: Optional[str] = None


class UserOut(UserResponse):
    role: Role
    password: Optional[str] = None
    refresh_token: Optional[str] = None
    github_token: Optional[str] = None
