from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.responses import ORJSONResponse

from app.core.auth import (
    GitHubOAuthDeps,
    GoogleOAuthDeps,
    PasswordOAuthDeps,
    UserAuthDeps,
)
from app.core.container import Container
from app.core.router import CoreAPIRouter
from app.schemas.users import UserOut, UserPasswordRequest, UserRequest, UserResponse
from app.services.auth import AuthService
from app.services.users import UserService

router = CoreAPIRouter(prefix="/user", tags=["user"])


@router.put(
    "",
    response_model=UserResponse,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[PasswordOAuthDeps, GoogleOAuthDeps, GitHubOAuthDeps],
    summary="",
    description="",
)
@inject
async def put_user(
    schema: UserRequest,
    user: Annotated[UserOut, UserAuthDeps],
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.put_by_id(id=user.id, schema=schema)


@router.patch(
    "",
    response_model=UserResponse,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[PasswordOAuthDeps, GoogleOAuthDeps, GitHubOAuthDeps],
    summary="",
    description="",
)
@inject
async def patch_user(
    schema: UserPasswordRequest,
    user: Annotated[UserOut, UserAuthDeps],
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await service.patch_password_by_id(user_id=user.id, schema=schema)


@router.delete(
    "",
    response_model=UserResponse,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[PasswordOAuthDeps, GoogleOAuthDeps, GitHubOAuthDeps],
    summary="",
    description="",
)
@inject
async def delete_user(
    user: Annotated[UserOut, UserAuthDeps],
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.delete_by_id(id=user.id)
