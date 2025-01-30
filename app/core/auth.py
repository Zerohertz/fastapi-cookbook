from typing import Annotated, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer

from app.core.container import Container
from app.exceptions.auth import NotAuthenticated
from app.models.enums import Role
from app.schemas.auth import JwtAccessToken
from app.schemas.users import UserOut
from app.services.users import UserService


class JwtBearer(HTTPBearer):
    def __init__(
        self,
        *,
        bearerFormat: Optional[str] = None,
        scheme_name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        super().__init__(
            bearerFormat=bearerFormat,
            scheme_name=scheme_name,
            description=description,
            auto_error=True,
        )

    async def __call__(self, request: Request) -> str:  # type: ignore[override]
        try:
            authorization = await super().__call__(request)
        except HTTPException as error:
            raise NotAuthenticated from error
        if authorization is None:
            raise NotAuthenticated
        return authorization.credentials


jwt_bearer = JwtBearer()


@inject
async def get_current_user(
    access_token: Annotated[str, Depends(jwt_bearer)],
    service: UserService = Depends(Provide[Container.user_service]),
) -> UserOut:
    token = JwtAccessToken(access_token=access_token)
    return await service.verify(token=token)


AuthDeps = Annotated[UserOut, Depends(get_current_user)]


async def get_admin_user(user: AuthDeps) -> UserOut:
    if user.role != Role.ADMIN:
        raise NotAuthenticated
    return user


AdminDeps = Depends(get_admin_user)
