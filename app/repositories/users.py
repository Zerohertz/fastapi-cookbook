from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.models.users import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session=session, model=User)
