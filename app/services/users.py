from app.models.users import User
from app.repositories.users import UserRepository
from app.schemas.users import UserIn, UserOut
from app.services.base import BaseService


class UserService(BaseService[User, UserIn, UserOut]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(repository=user_repository, schema=UserOut)
        self.repository: UserRepository

    async def get_all(self) -> list[UserOut]:
        users = await self.repository.read_all()
        schemas = []
        for user in users:
            schemas.append(self.mapper(user))
        return schemas
