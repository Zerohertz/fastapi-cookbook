from datetime import datetime, timedelta

import httpx
import pytz
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from loguru import logger
from passlib.exc import UnknownHashError
from pydantic import ValidationError

from app.core.configs import configs
from app.core.database import database
from app.exceptions.auth import (
    GitHubOAuthFailed,
    GoogleOAuthFailed,
    NotAuthenticated,
    NotRegistered,
    OAuthFormDataInvalid,
    PasswordOAuthFailed,
    TokenDecodeError,
    TokenExpired,
    UserAlreadyExists,
)
from app.exceptions.database import EntityNotFound
from app.models.auth import OAuth
from app.models.enums import OAuthProvider, Role
from app.models.users import User
from app.repositories.auth import AuthRepository
from app.repositories.users import UserRepository
from app.schemas.auth import (
    AuthIn,
    AuthOut,
    GitHubOAuthRequest,
    GitHubOAuthToken,
    GitHubOAuthUser,
    GoogleOAuthRequest,
    GoogleOAuthToken,
    GoogleOAuthUser,
    JwtAccessToken,
    JwtPayload,
    JwtToken,
    OAuthResponse,
    PasswordOAuthReigsterRequest,
    PasswordOAuthRequest,
    RefreshOAuthRequest,
)
from app.schemas.users import UserIn, UserOut
from app.services.base import BaseMapper, BaseService
from app.services.security import CryptService


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

    def create_token(self, user: User) -> JwtToken:
        return JwtToken(
            access_token=self.create_access_token(user),
            refresh_token=self.create_refresh_token(user),
            token_type="bearer",
            expires_in=self.access_expire.seconds,
        )

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
        try:
            google_oauth_token = GoogleOAuthToken.model_validate(response.json())
        except ValidationError as error:
            logger.error(response.json())
            raise GoogleOAuthFailed from error
        return google_oauth_token

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
        try:
            google_oauth_user = GoogleOAuthUser.model_validate(response.json())
        except ValidationError as error:
            logger.error(response.json())
            raise GoogleOAuthFailed from error
        return google_oauth_user

    async def get_token_and_user(self, schema: GoogleOAuthRequest) -> OAuthResponse:
        google_oauth_token = await self._get_token(schema=schema)
        google_oauth_user = await self._get_user(schema=google_oauth_token)
        return OAuthResponse(
            id=google_oauth_user.id,
            token=google_oauth_token.access_token,
            name=google_oauth_user.name,
            email=google_oauth_user.email,
        )


class GitHubService:
    def __init__(self) -> None:
        self.client_id = configs.GITHUB_OAUTH_CLIENT_ID
        self.client_secret = configs.GITHUB_OAUTH_CLIENT_SECRET

    async def _get_token(self, schema: GitHubOAuthRequest) -> GitHubOAuthToken:
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
                logger.error(response.json())
                raise GitHubOAuthFailed from error
        try:
            github_oauth_token = GitHubOAuthToken.model_validate(response.json())
        except ValidationError as error:
            logger.error(response.json())
            raise GitHubOAuthFailed from error
        return github_oauth_token

    async def _get_user(self, schema: GitHubOAuthToken) -> GitHubOAuthUser:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "https://api.github.com/user",
                    headers={
                        "Accept": "application/json",
                        "Authorization": f"Bearer {schema.access_token}",
                    },
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as error:
                logger.error(response.json())
                raise GitHubOAuthFailed from error
        github_oauth_user = response.json()
        github_oauth_user["id"] = str(github_oauth_user["id"])
        try:
            github_oauth_user = GitHubOAuthUser.model_validate(github_oauth_user)
        except ValidationError as error:
            logger.error(response.json())
            raise GitHubOAuthFailed from error
        return github_oauth_user

    async def get_token_and_user(self, schema: GitHubOAuthRequest) -> OAuthResponse:
        github_oauth_token = await self._get_token(schema=schema)
        github_oauth_user = await self._get_user(github_oauth_token)
        return OAuthResponse(
            id=github_oauth_user.id,
            token=github_oauth_token.access_token,
            name=github_oauth_user.name,
            email=github_oauth_user.email,
        )


class AuthService(BaseService[OAuth, AuthIn, AuthOut]):
    def __init__(
        self,
        auth_repository: AuthRepository,
        user_repository: UserRepository,
        jwt_service: JwtService,
        crypt_service: CryptService,
    ):
        super().__init__(repository=auth_repository, schema=AuthOut)
        self.repository: AuthRepository
        self.user_repository = user_repository
        self.user_mapper = BaseMapper[User, UserIn, UserOut](model=User, schema=UserOut)
        self.jwt_service = jwt_service
        self.crypt_service = crypt_service
        self.google_service = GoogleService()
        self.github_service = GitHubService()

    def _create_token(self, user: User) -> JwtToken:
        jwt_token = self.jwt_service.create_token(user)
        user.refresh_token = jwt_token.refresh_token
        return jwt_token

    @database.transactional
    async def _log_in_oauth(
        self, schema: OAuthResponse, provider: OAuthProvider
    ) -> JwtToken:
        oauth = await self.repository.read_by_oauth_id_and_provider(
            oauth_id=schema.id, provider=provider
        )
        if oauth:
            return self._create_token(user=oauth.user)
        user = await self.user_repository.read_by_email(schema.email)
        oauth = OAuth(
            provider=provider,
            oauth_id=schema.id,
            oauth_token=schema.token,
        )
        if not user:
            user = User(
                name=schema.name, email=schema.email, role=Role.USER, refresh_token=None
            )
        user.oauth.append(oauth)
        user = await self.user_repository.create(entity=user)
        return self._create_token(user=user)

    @database.transactional
    async def register(self, schema: PasswordOAuthReigsterRequest) -> UserOut:
        if schema.grant_type != OAuthProvider.PASSWORD.value:
            raise OAuthFormDataInvalid
        user = await self.user_repository.read_by_email(email=schema.username)
        oauth = None
        if user:
            for _oauth in user.oauth:
                if _oauth.provider != OAuthProvider.PASSWORD:
                    continue
                oauth = _oauth
                break
            if oauth:
                raise UserAlreadyExists
        oauth = OAuth(
            provider=OAuthProvider.PASSWORD,
            password=self.crypt_service.hash(schema.password),
        )
        if not user:
            user = User(
                name=schema.name,
                email=schema.username,
                role=Role.USER,
                refresh_token=None,
            )
        user.oauth.append(oauth)
        user = await self.user_repository.create(entity=user)
        return self.user_mapper(user)

    @database.transactional
    async def log_in_password(self, schema: PasswordOAuthRequest) -> JwtToken:
        if schema.grant_type != OAuthProvider.PASSWORD.value:
            raise OAuthFormDataInvalid
        user = await self.user_repository.read_by_email(schema.username)
        if not user:
            raise NotRegistered
        oauth = None
        for _oauth in user.oauth:
            if _oauth.provider != OAuthProvider.PASSWORD:
                continue
            oauth = _oauth
            break
        if not oauth:
            # TODO: 다른 OAuth로 등록 되어 있음을 밝혀야함
            raise NotRegistered
        try:
            is_verified = self.crypt_service.verify(schema.password, oauth.password)
        except UnknownHashError as error:
            # TODO: 언제 UnknownHashError가 발생하는지 확인
            raise PasswordOAuthFailed from error
        if not is_verified:
            raise PasswordOAuthFailed
        jwt_token = self.jwt_service.create_token(user)
        user.refresh_token = jwt_token.refresh_token
        return jwt_token

    @database.transactional
    async def log_in_google(self, schema: GoogleOAuthRequest) -> JwtToken:
        oauth_response = await self.google_service.get_token_and_user(schema=schema)
        return await self._log_in_oauth(oauth_response, OAuthProvider.GOOGLE)

    @database.transactional
    async def log_in_github(self, schema: GitHubOAuthRequest) -> JwtToken:
        oauth_response = await self.github_service.get_token_and_user(schema=schema)
        return await self._log_in_oauth(oauth_response, OAuthProvider.GITHUB)

    @database.transactional
    async def verify(self, schema: JwtAccessToken) -> UserOut:
        user_id = int(self.jwt_service.decode(token=schema.access_token))
        try:
            user = await self.user_repository.read_by_id(id=user_id)
        except EntityNotFound as error:
            raise NotAuthenticated from error
        user.refresh_token = self.jwt_service.create_refresh_token(user)
        return self.user_mapper(user)

    async def refresh(self, schema: RefreshOAuthRequest) -> JwtToken:
        if schema.grant_type != "refresh_token":
            raise OAuthFormDataInvalid
        sub = self.jwt_service.decode(token=schema.refresh_token)
        if ".refresh" not in sub:
            raise TokenDecodeError
        user_id = int(sub.split(".")[0])
        user = await self.user_repository.read_by_id(user_id)
        return JwtToken(
            access_token=self.jwt_service.create_access_token(user),
            refresh_token=schema.refresh_token,
            token_type="bearer",
            expires_in=self.jwt_service.access_expire.seconds,
        )
