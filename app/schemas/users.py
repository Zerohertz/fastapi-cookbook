from typing import Optional

from app.schemas.base import BaseSchemaRequest, BaseSchemaResponse


class UserRequest(BaseSchemaRequest):
    name: str
    email: str


class UserRegisterRequest(UserRequest):
    password: str


class UserPasswordRequest(BaseSchemaRequest):
    email: str
    password: str


class UserResponse(BaseSchemaResponse):
    name: str
    email: str
    oauth: str


class UserIn(UserRequest):
    oauth: str
    password: Optional[str] = None
    refresh_token: Optional[str] = None
    github_token: Optional[str] = None


class UserOut(UserResponse):
    password: Optional[str] = None
    refresh_token: Optional[str] = None
    github_token: Optional[str] = None
