from typing import overload

from app.models.users import User
from app.repositories.users import UserRepository
from app.schemas.base import BaseSchemaRequest, BaseSchemaResponse
from app.schemas.users import UserCreateResponse
from app.services.base import BaseService


class UserService(BaseService[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)

    @overload
    def mapper(self, data: BaseSchemaRequest) -> User: ...

    @overload
    def mapper(self, data: User) -> BaseSchemaResponse: ...

    def mapper(self, data: BaseSchemaRequest | User) -> User | BaseSchemaResponse:
        if isinstance(data, BaseSchemaRequest):
            return self.repository.model(**data.model_dump())
        return UserCreateResponse.model_validate(data)
