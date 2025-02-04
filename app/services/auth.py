from datetime import datetime, timedelta

import httpx
import pytz
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from loguru import logger
from passlib.context import CryptContext

from app.core.configs import configs
from app.exceptions.auth import (
    GitHubOAuthFailed,
    GoogleOAuthFailed,
    OAuthFormDataInvalid,
    TokenDecodeError,
    TokenExpired,
)
from app.models.users import User
from app.schemas.auth import (
    GitHubOAuthRequest,
    GoogleOAuthRequest,
    GoogleOAuthToken,
    GoogleOAuthUser,
    JwtPayload,
    OAuthResponse,
)


class CryptService(CryptContext):
    def __init__(self) -> None:
        super().__init__(schemes=["bcrypt"], deprecated="auto")

    def hash(self, secret: str) -> str:  # type: ignore[override]
        return super().hash(secret=secret)

    def verify(self, secret: str, hash: str) -> bool:  # type: ignore[override]
        return super().verify(secret=secret, hash=hash)


class JwtService:
    def __init__(self) -> None:
        self.secret = configs.JWT_SECRET_KEY
        self.algorithm = configs.JWT_ALGORITHM
        self.access_expire = timedelta(hours=2)
        self.refresh_expire = timedelta(days=1)

    def _encode(self, *, sub: str, exp: timedelta) -> str:
        payload = JwtPayload(
            sub=sub,
            iat=datetime.now().astimezone(pytz.timezone(configs.TZ)),
            exp=datetime.now().astimezone(pytz.timezone(configs.TZ)) + exp,
        )
        return jwt.encode(
            claims=payload.model_dump(), key=self.secret, algorithm=self.algorithm
        )

    def create_access_token(self, user: User) -> str:
        return self._encode(sub=str(user.id), exp=self.access_expire)

    def create_refresh_token(self, user: User) -> str:
        return self._encode(sub=f"{user.id}.refresh", exp=self.refresh_expire)

    def decode(self, *, token: str) -> str:
        try:
            payload = jwt.decode(
                token=token, key=self.secret, algorithms=self.algorithm
            )
            return payload["sub"]
        except ExpiredSignatureError as error:
            raise TokenExpired from error
        except JWTError as error:
            raise TokenDecodeError from error


class GoogleService:
    def __init__(self) -> None:
        self.client_id = configs.GOOGLE_OAUTH_CLIENT_ID
        self.client_secret = configs.GOOGLE_OAUTH_CLIENT_SECRET

    async def _get_token(self, schema: GoogleOAuthRequest) -> GoogleOAuthToken:
        if schema.grant_type != "authorization_code":
            raise OAuthFormDataInvalid
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://oauth2.googleapis.com/token",
                    json={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "grant_type": schema.grant_type,
                        "code": schema.code,
                        "redirect_uri": schema.redirect_uri,
                    },
                    headers={"Accept": "application/json"},
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as error:
                logger.error(response.json())
                raise GoogleOAuthFailed from error
        return GoogleOAuthToken.model_validate(response.json())

    async def _get_user(self, schema: GoogleOAuthToken) -> GoogleOAuthUser:
        # https://developers.google.com/identity/protocols/oauth2/scopes#oauth2
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "https://www.googleapis.com/oauth2/v2/userinfo",
                    headers={
                        "Accept": "application/json",
                        "Authorization": f"Bearer {schema.access_token}",
                    },
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as error:
                logger.error(response.json())
                raise GoogleOAuthFailed from error
        return GoogleOAuthUser.model_validate(response.json())

    async def get_token_and_user(self, schema: GoogleOAuthRequest) -> OAuthResponse:
        google_oauth_token = await self._get_token(schema=schema)
        google_oauth_user = await self._get_user(schema=google_oauth_token)
        return OAuthResponse(
            token=google_oauth_token.access_token,
            name=google_oauth_user.name,
            email=google_oauth_user.email,
        )


class GitHubService:
    def __init__(self) -> None:
        self.client_id = configs.GITHUB_OAUTH_CLIENT_ID
        self.client_secret = configs.GITHUB_OAUTH_CLIENT_SECRET

    async def get_token_and_user(self, schema: GitHubOAuthRequest) -> OAuthResponse:
        if schema.grant_type != "authorization_code":
            raise OAuthFormDataInvalid
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://github.com/login/oauth/access_token",
                    json={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "code": schema.code,
                        "redirect_uri": schema.redirect_uri,
                    },
                    headers={"Accept": "application/json"},
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as error:
                raise GitHubOAuthFailed from error
        data = response.json()
        github_token = data.get("access_token", None)
        if github_token is None:
            raise GitHubOAuthFailed
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "https://api.github.com/user",
                    headers={
                        "Accept": "application/json",
                        "Authorization": f"Bearer {github_token}",
                    },
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as error:
                raise GitHubOAuthFailed from error
        github_user = response.json()
        github_name, github_email = github_user.get("login", None), github_user.get(
            "email", None
        )
        if github_name is None or github_email is None:
            raise GitHubOAuthFailed
        return OAuthResponse(token=github_token, name=github_name, email=github_email)
