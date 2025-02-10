from app.core.database import database
from app.models.users import User
from app.repositories.users import UserRepository
from app.schemas.users import UserOut, UserPatchRequest
from app.services.base import BaseService
from app.services.security import CryptService


class UserService(BaseService[User]):
    def __init__(self, user_repository: UserRepository, crypt_service: CryptService):
        super().__init__(repository=user_repository, schema=UserOut)
        self.repository: UserRepository
        self.crypt_service = crypt_service

    async def get_all(self) -> list[UserOut]:
        users = await self.repository.read_all()
        schemas = []
        for user in users:
            schemas.append(self.mapper(user))
        return schemas

    @database.transactional
    async def patch_by_id(self, id: int, schema: UserPatchRequest) -> UserOut:
        if schema.password:
            schema.password = self.crypt_service.hash(schema.password)
        user = await self.repository.update_by_id(
            id=id, data=schema.model_dump(exclude_none=True)
        )
        return self.mapper(user)
