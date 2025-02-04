from typing import overload

from passlib.exc import UnknownHashError

from app.core.database import database
from app.exceptions.auth import (
    NotAuthenticated,
    NotRegistered,
    OAuthFormDataInvalid,
    PasswordOAuthFailed,
    TokenDecodeError,
    UserAlreadyExists,
)
from app.exceptions.database import EntityNotFound
from app.models.enums import OAuthProvider, Role
from app.models.users import User
from app.repositories.users import UserRepository
from app.schemas.auth import (
    GitHubOAuthRequest,
    GoogleOAuthRequest,
    JwtAccessToken,
    JwtToken,
    OAuthResponse,
    PasswordOAuthReigsterRequest,
    PasswordOAuthRequest,
    RefreshOAuthRequest,
)
from app.schemas.base import BaseRequest
from app.schemas.users import UserIn, UserOut, UserPatchRequest, UserResponse
from app.services.auth import CryptService, GitHubService, GoogleService, JwtService
from app.services.base import BaseService


class UserService(BaseService[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)
        self.repository: UserRepository
        self.crypt_service = CryptService()
        self.jwt_service = JwtService()
        self.google_service = GoogleService()
        self.github_service = GitHubService()

    @overload
    def mapper(self, data: BaseRequest) -> User: ...

    @overload
    def mapper(self, data: User) -> UserResponse: ...

    def mapper(self, data: BaseRequest | User) -> User | UserResponse:
        if isinstance(data, BaseRequest):
            return self.repository.model(**data.model_dump())
        return UserResponse.model_validate(data)

    async def get_all(self) -> list[UserResponse]:
        entities = await self.repository.read_all()
        schemas = []
        for entity in entities:
            schemas.append(self.mapper(entity))
        return schemas

    @database.transactional
    async def patch_by_id(self, id: int, schema: UserPatchRequest) -> UserResponse:
        if schema.password:
            schema.password = self.crypt_service.hash(schema.password)
        entity = await self.repository.update_by_id(
            id=id, data=schema.model_dump(exclude_none=True)
        )
        return self.mapper(entity)

    @database.transactional
    async def register(self, schema: PasswordOAuthReigsterRequest) -> UserResponse:
        if schema.grant_type != "password":
            raise OAuthFormDataInvalid
        entity = await self.repository.read_by_name_or_email(
            name=schema.name, email=schema.username
        )
        if entity:
            raise UserAlreadyExists
        _schema = UserIn(
            name=schema.name,
            email=schema.username,
            role=Role.USER,
            oauth=OAuthProvider.PASSWORD,
            password=self.crypt_service.hash(schema.password),
            refresh_token=None,
            oauth_token=None,
        )
        entity = self.mapper(_schema)
        entity = await self.repository.create(entity=entity)
        return self.mapper(entity)

    @database.transactional
    async def log_in_password(self, schema: PasswordOAuthRequest) -> JwtToken:
        if schema.grant_type != "password":
            raise OAuthFormDataInvalid
        entity = await self.repository.read_by_email(schema.username)
        if not entity:
            raise NotRegistered
        if entity.oauth != "password":
            # TODO: 다른 OAuth로 로그인 했음을 밝혀야함
            pass
        try:
            is_verified = self.crypt_service.verify(schema.password, entity.password)
        except UnknownHashError as error:
            # TODO: 언제 UnknownHashError가 발생하는지 확인
            raise PasswordOAuthFailed from error
        if not is_verified:
            raise PasswordOAuthFailed
        access_token, refresh_token = self.jwt_service.create_access_token(
            entity
        ), self.jwt_service.create_refresh_token(entity)
        entity.refresh_token = refresh_token
        jwt_token = JwtToken(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.jwt_service.access_expire.seconds,
        )
        return jwt_token

    @database.transactional
    async def _log_in_oauth(
        self, schema: OAuthResponse, oauth: OAuthProvider
    ) -> JwtToken:
        entity = await self.repository.read_by_name(name=schema.name)
        if entity:
            access_token, refresh_token = self.jwt_service.create_access_token(
                entity
            ), self.jwt_service.create_refresh_token(entity)
            entity.refresh_token = refresh_token
            return JwtToken(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=self.jwt_service.access_expire.seconds,
            )
        _schema = UserIn(
            name=schema.name,
            email=schema.email,
            role=Role.USER,
            oauth=oauth,
            password=None,
            refresh_token=None,
            oauth_token=schema.token,
        )
        entity = self.mapper(_schema)
        entity = await self.repository.create(entity=entity)
        access_token, refresh_token = self.jwt_service.create_access_token(
            entity
        ), self.jwt_service.create_refresh_token(entity)
        entity.refresh_token = refresh_token
        jwt_token = JwtToken(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.jwt_service.access_expire.seconds,
        )
        return jwt_token

    @database.transactional
    async def log_in_google(self, schema: GoogleOAuthRequest) -> JwtToken:
        oauth_response = await self.google_service.get_token_and_user(schema=schema)
        return await self._log_in_oauth(oauth_response, OAuthProvider.GOOGLE)

    @database.transactional
    async def log_in_github(self, schema: GitHubOAuthRequest) -> JwtToken:
        oauth_response = await self.github_service.get_token_and_user(schema=schema)
        entity = await self.repository.read_by_name(name=oauth_response.name)
        if entity:
            access_token, refresh_token = self.jwt_service.create_access_token(
                entity
            ), self.jwt_service.create_refresh_token(entity)
            entity.refresh_token = refresh_token
            return JwtToken(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=self.jwt_service.access_expire.seconds,
            )
        _schema = UserIn(
            name=oauth_response.name,
            email=oauth_response.email,
            role=Role.USER,
            oauth=OAuthProvider.GITHUB,
            password=None,
            refresh_token=None,
            oauth_token=oauth_response.token,
        )
        entity = self.mapper(_schema)
        entity = await self.repository.create(entity=entity)
        access_token, refresh_token = self.jwt_service.create_access_token(
            entity
        ), self.jwt_service.create_refresh_token(entity)
        entity.refresh_token = refresh_token
        jwt_token = JwtToken(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.jwt_service.access_expire.seconds,
        )
        return jwt_token

    @database.transactional
    async def verify(self, schema: JwtAccessToken) -> UserOut:
        user_id = int(self.jwt_service.decode(token=schema.access_token))
        try:
            entity = await self.repository.read_by_id(user_id)
        except EntityNotFound as error:
            raise NotAuthenticated from error
        entity.refresh_token = self.jwt_service.create_refresh_token(entity)
        return UserOut.model_validate(entity)

    async def refresh(self, schema: RefreshOAuthRequest) -> JwtToken:
        if schema != "refresh_token":
            raise OAuthFormDataInvalid
        sub = self.jwt_service.decode(token=schema.refresh_token)
        if ".refresh" not in sub:
            raise TokenDecodeError
        user_id = int(sub.split(".")[0])
        entity = await self.repository.read_by_id(user_id)
        return JwtToken(
            access_token=self.jwt_service.create_access_token(entity),
            refresh_token=sub,
            expires_in=self.jwt_service.access_expire.seconds,
        )
