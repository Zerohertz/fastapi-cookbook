from sqlalchemy import select

from app.core.database import database
from app.models.auth import OAuth
from app.models.enums import OAuthProvider
from app.repositories.base import BaseRepository


class AuthRepository(BaseRepository[OAuth]):
    def __init__(self):
        super().__init__(model=OAuth)

    async def read_by_user_id_and_password(
        self, user_id: int, eager: bool = False
    ) -> OAuth | None:
        stmt = select(self.model)
        stmt = stmt.where(
            self.model.user_id == user_id, self.model.provider == OAuthProvider.PASSWORD
        )
        if eager:
            stmt = self._eager(stmt=stmt)
        session = database.scoped_session()
        result = await session.execute(stmt)
        entity = result.scalar_one_or_none()
        return entity

    async def read_by_oauth_id_and_provider(
        self, oauth_id: str, provider: OAuthProvider, eager: bool = False
    ) -> OAuth | None:
        stmt = select(self.model)
        stmt = stmt.where(
            self.model.oauth_id == oauth_id, self.model.provider == provider
        )
        if eager:
            stmt = self._eager(stmt=stmt)
        session = database.scoped_session()
        result = await session.execute(stmt)
        entity = result.scalar_one_or_none()
        return entity
