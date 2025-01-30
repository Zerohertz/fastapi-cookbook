from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import or_

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

    async def read_by_name(self, name: str, eager: bool = False) -> Optional[User]:
        stmt = select(self.model)
        if eager:
            stmt = self._eager(stmt)
        stmt = stmt.filter(self.model.name == name)
        session = database.scoped_session()
        result = await session.execute(stmt)
        entity = result.scalar_one_or_none()
        return entity

    async def read_by_email(self, email: str, eager: bool = False) -> Optional[User]:
        stmt = select(self.model)
        if eager:
            for _eager in getattr(self.model, "eagers"):
                stmt = stmt.options(joinedload(getattr(self.model, _eager)))
        stmt = stmt.filter(self.model.email == email)
        session = database.scoped_session()
        result = await session.execute(stmt)
        entity = result.scalar_one_or_none()
        return entity

    async def read_by_name_or_email(self, name: str, email: str) -> Optional[User]:
        stmt = select(self.model)
        stmt = stmt.filter(or_(self.model.name == name, self.model.email == email))
        session = database.scoped_session()
        result = await session.execute(stmt)
        entity = result.scalar_one_or_none()
        return entity
