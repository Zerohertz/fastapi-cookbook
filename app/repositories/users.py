from app.models.users import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(model=User)
