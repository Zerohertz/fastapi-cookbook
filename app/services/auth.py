from datetime import datetime, timedelta

import httpx
import pytz
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from passlib.context import CryptContext

from app.core.configs import configs
from app.exceptions.auth import GitHubOAuth, TokenDecode, TokenExpired
from app.models.users import User
from app.schemas.auth import JwtPayload


class CryptService:
    def __init__(self) -> None:
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, secret: str) -> str:
        return self.context.hash(secret=secret)

    def verify(self, secret: str, hash: str) -> bool:
        return self.context.verify(secret=secret, hash=hash)


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
        except JWTError:
            raise TokenDecode
        except ExpiredSignatureError:
            raise TokenExpired


class GitHubService:
    def __init__(self) -> None:
        self.client_id = configs.GITHUB_OAUTH_CLIENT_ID
        self.client_secret = configs.GITHUB_OAUTH_CLIENT_SECRET

    async def get_user(self, code: str) -> tuple[str, str, str]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://github.com/login/oauth/access_token",
                    json={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "code": code,
                    },
                    headers={"Accept": "application/json"},
                )
                response.raise_for_status()
                github_token = response.json()["access_token"]
                response = await client.get(
                    "https://api.github.com/user",
                    headers={
                        "Accept": "application/json",
                        "Authorization": f"Bearer {github_token}",
                    },
                )
                response.raise_for_status()
                github_user = response.json()
            except httpx.HTTPStatusError:
                raise GitHubOAuth
        return github_token, github_user["login"], github_user["email"]
