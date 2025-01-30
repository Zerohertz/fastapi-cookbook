from typing import overload

from passlib.exc import UnknownHashError

from app.core.database import database
from app.exceptions.auth import (
    LoginFailed,
    NotAuthenticated,
    NotRegistered,
    UserAlreadyExists,
)
from app.exceptions.database import EntityNotFound
from app.models.enums import OAuthProvider, Role
from app.models.users import User
from app.repositories.users import UserRepository
from app.schemas.auth import JwtAccessToken, JwtRefreshToken, JwtToken
from app.schemas.base import BaseRequest
from app.schemas.users import (
    UserIn,
    UserOut,
    UserPasswordRequest,
    UserPatchRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.services.auth import CryptService, GitHubService, JwtService
from app.services.base import BaseService


class UserService(BaseService[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)
        self.repository: UserRepository
        self.crypt_service = CryptService()
        self.jwt_service = JwtService()
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
    async def register(self, schema: UserRegisterRequest) -> UserResponse:
        entity = await self.repository.read_by_name_or_email(
            name=schema.name, email=schema.email
        )
        if entity:
            raise UserAlreadyExists
        _schema = UserIn(
            name=schema.name,
            email=schema.email,
            role=Role.USER,
            oauth=OAuthProvider.PASSWORD,
            password=self.crypt_service.hash(schema.password),
            refresh_token=None,
            github_token=None,
        )
        entity = self.mapper(_schema)
        entity = await self.repository.create(entity=entity)
        return self.mapper(entity)

    @database.transactional
    async def log_in_password(self, schema: UserPasswordRequest) -> JwtToken:
        entity = await self.repository.read_by_email(schema.email)
        if not entity:
            raise NotRegistered
        if entity.oauth != "password":
            # TODO: 다른 OAuth로 로그인 했음을 밝혀야함
            pass
        try:
            is_verified = self.crypt_service.verify(schema.password, entity.password)
        except UnknownHashError as error:
            # TODO: 언제 UnknownHashError가 발생하는지 확인
            raise LoginFailed from error
        if not is_verified:
            raise LoginFailed
        access_token, refresh_token = self.jwt_service.create_access_token(
            entity
        ), self.jwt_service.create_refresh_token(entity)
        entity.refresh_token = refresh_token
        jwt_token = JwtToken(access_token=access_token, refresh_token=refresh_token)
        return jwt_token

    @database.transactional
    async def log_in_github(self, code: str) -> JwtToken:
        github_token, github_name, github_email = await self.github_service.get_user(
            code
        )
        entity = await self.repository.read_by_name(name=github_name)
        if entity:
            access_token, refresh_token = self.jwt_service.create_access_token(
                entity
            ), self.jwt_service.create_refresh_token(entity)
            entity.refresh_token = refresh_token
            return JwtToken(access_token=access_token, refresh_token=refresh_token)
        schema = UserIn(
            name=github_name,
            email=github_email,
            role=Role.USER,
            oauth=OAuthProvider.GITHUB,
            password=None,
            refresh_token=None,
            github_token=github_token,
        )
        entity = self.mapper(schema)
        entity = await self.repository.create(entity=entity)
        access_token, refresh_token = self.jwt_service.create_access_token(
            entity
        ), self.jwt_service.create_refresh_token(entity)
        entity.refresh_token = refresh_token
        jwt_token = JwtToken(access_token=access_token, refresh_token=refresh_token)
        return jwt_token

    @database.transactional
    async def verify(self, token: JwtAccessToken) -> UserOut:
        user_id = int(self.jwt_service.decode(token=token.access_token))
        try:
            entity = await self.repository.read_by_id(user_id)
        except EntityNotFound as error:
            raise NotAuthenticated from error
        entity.refresh_token = self.jwt_service.create_refresh_token(entity)
        return UserOut.model_validate(entity)

    async def refresh(self, token: JwtRefreshToken) -> JwtAccessToken:
        user_id = int(self.jwt_service.decode(token=token.refresh_token).split(".")[0])
        entity = await self.repository.read_by_id(user_id)
        return JwtAccessToken(access_token=self.jwt_service.create_access_token(entity))
