from typing import AsyncContextManager, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Callable[..., AsyncContextManager[AsyncSession]]):
        super().__init__(session=session, model=User)
