from typing import Optional

from sqlalchemy import select

from app.core.database import database
from app.models.auth import OAuth
from app.models.enums import OAuthProvider
from app.repositories.base import BaseRepository


class AuthRepository(BaseRepository[OAuth]):
    def __init__(self):
        super().__init__(model=OAuth)

    async def read_by_oauth_id_and_provider(
        self, oauth_id: str, provider: OAuthProvider
    ) -> Optional[OAuth]:
        stmt = select(self.model)
        stmt = stmt.where(
            self.model.oauth_id == oauth_id, self.model.provider == provider
        )
        stmt = self._eager(stmt=stmt)
        session = database.scoped_session()
        result = await session.execute(stmt)
        entity = result.scalar_one_or_none()
        return entity
