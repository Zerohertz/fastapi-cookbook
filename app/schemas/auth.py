from datetime import datetime

from pydantic import BaseModel


class JwtPayload(BaseModel):
    sub: str
    iat: datetime
    exp: datetime


class JwtAccessToken(BaseModel):
    access_token: str


class JwtRefreshToken(BaseModel):
    refresh_token: str


class JwtToken(JwtAccessToken, JwtRefreshToken): ...
