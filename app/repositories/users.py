from typing import Sequence

from sqlalchemy import select

from app.core.database import database
from app.exceptions.database import EntityNotFound
from app.models.users import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(model=User)

    async def read_all(self) -> Sequence[User]:
        stmt = select(self.model)
        session = database.scoped_session()
        result = await session.execute(stmt)
        entity = result.scalars().all()
        if not entity:
            raise EntityNotFound
        return entity

    async def read_by_email(self, email: str) -> User | None:
        stmt = select(self.model)
        stmt = stmt.where(self.model.email == email)
        session = database.scoped_session()
        result = await session.execute(stmt)
        entity = result.scalar_one_or_none()
        return entity
