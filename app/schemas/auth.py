from datetime import datetime
from typing import Annotated

from fastapi import Form
from pydantic import BaseModel

from app.schemas.base import BaseRequest


class OAuthRequest(BaseRequest):
    grant_type: str


class RefreshOAuthRequest(OAuthRequest):
    grant_type: Annotated[str, Form(pattern="refresh_token")]
    refresh_token: Annotated[str, Form(...)]


class PasswordOAuthRequest(OAuthRequest):
    grant_type: Annotated[str, Form(pattern="password")]
    username: Annotated[
        str,
        Form(
            min_length=5,
            max_length=50,
            pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        ),
    ]
    password: Annotated[str, Form(min_length=8, max_length=30)]


class PasswordOAuthReigsterRequest(PasswordOAuthRequest):
    name: Annotated[str, Form(min_length=3, max_length=30)]


class GoogleOAuthRequest(OAuthRequest):
    grant_type: Annotated[str, Form(pattern="authorization_code")]
    code: Annotated[str, Form(...)]
    redirect_uri: Annotated[str, Form("")]


class GoogleOAuthToken(BaseModel):
    access_token: str
    expires_in: int
    scope: str
    token_type: str
    id_token: str


class GoogleOAuthUser(BaseModel):
    id: str
    email: str
    verified_email: bool
    name: str
    given_name: str
    family_name: str
    picture: str


class GitHubOAuthRequest(OAuthRequest):
    grant_type: Annotated[str, Form(pattern="authorization_code")]
    code: Annotated[str, Form(...)]
    redirect_uri: Annotated[str, Form("")]


class GitHubOAuthToken(BaseModel):
    access_token: str
    token_type: str
    scope: str


class GitHubOAuthUser(BaseModel):
    id: int
    login: str
    avatar_url: str
    gravatar_id: str
    html_url: str
    name: str
    company: str
    blog: str
    location: str
    email: str


class OAuthResponse(BaseModel):
    token: str
    name: str
    email: str


class JwtPayload(BaseModel):
    sub: str
    iat: datetime
    exp: datetime


class JwtAccessToken(BaseModel):
    access_token: str


class JwtToken(JwtAccessToken):
    # https://datatracker.ietf.org/doc/html/rfc6749#section-5.1
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
