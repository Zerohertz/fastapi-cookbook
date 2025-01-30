from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory

from app.repositories.users import UserRepository
from app.services.users import UserService


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        modules=[
            "app.core.auth",
            "app.api.v1.endpoints.users",
            "app.api.v1.endpoints.auth",
            "app.api.v1.endpoints.admin.users",
        ]
    )

    user_repository = Factory(UserRepository)

    user_service = Factory(UserService, user_repository=user_repository)
