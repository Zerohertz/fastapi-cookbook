from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory

from app.repositories.auth import AuthRepository
from app.repositories.users import UserRepository
from app.services.auth import AuthService, JwtService
from app.services.security import CryptService
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
    auth_repository = Factory(AuthRepository)

    jwt_service = Factory(JwtService)
    crypt_service = Factory(CryptService)
    user_service = Factory(
        UserService, user_repository=user_repository, crypt_service=crypt_service
    )
    auth_service = Factory(
        AuthService,
        auth_repository=auth_repository,
        user_repository=user_repository,
        jwt_service=jwt_service,
        crypt_service=crypt_service,
    )
