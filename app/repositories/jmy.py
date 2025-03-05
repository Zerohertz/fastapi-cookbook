from sqlalchemy import select

from app.core.database import database
from app.models.jmy import JmyCompany
from app.repositories.base import BaseRepository


class JmyRepository(BaseRepository[JmyCompany]):
    def __init__(self):
        super().__init__(model=JmyCompany)

    async def read_by_name(self, name: str, eager: bool = False) -> JmyCompany | None:
        stmt = select(self.model)
        if eager:
            stmt = self._eager(stmt=stmt)
        stmt = stmt.where(self.model.name == name)
        session = database.scoped_session()
        result = await session.execute(stmt)
        entity = result.scalar_one_or_none()
        return entity
