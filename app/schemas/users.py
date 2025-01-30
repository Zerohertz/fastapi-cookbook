from typing import Optional

from app.models.enums import OAuthProvider, Role
from app.schemas.base import BaseSchemaRequest, BaseSchemaResponse


class UserRequest(BaseSchemaRequest):
    name: str
    email: str


class UserRegisterRequest(UserRequest):
    password: str


class UserPasswordRequest(BaseSchemaRequest):
    email: str
    password: str


class UserPatchRequest(BaseSchemaRequest):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserResponse(BaseSchemaResponse):
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
