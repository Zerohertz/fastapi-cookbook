from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.core.database import Database
from app.repositories.users import UserRepository
from app.services.users import UserService


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["app.api.v1.endpoints.users"])

    database = Singleton(Database)

    user_repository = Factory(UserRepository, session=database.provided.session)

    user_service = Factory(UserService, user_repository=user_repository)