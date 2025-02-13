from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.responses import ORJSONResponse

from app.core.auth import (
    AdminAuthDeps,
    GitHubOAuthDeps,
    GoogleOAuthDeps,
    PasswordOAuthDeps,
)
from app.core.container import Container
from app.core.router import CoreAPIRouter
from app.schemas.users import UserOut, UserPasswordAdminRequest, UserRequest
from app.services.auth import AuthService
from app.services.users import UserService

router = CoreAPIRouter(
    prefix="/user",
    tags=["admin"],
    dependencies=[AdminAuthDeps, PasswordOAuthDeps, GoogleOAuthDeps, GitHubOAuthDeps],
)


@router.get(
    "",
    response_model=list[UserOut],
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
@inject
async def get_users(
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.get_all()


@router.get(
    "/{id}",
    response_model=UserOut,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
@inject
async def get_user(
    id: int,
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.get_by_id(id=id)


@router.put(
    "/{id}",
    response_model=UserOut,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
@inject
async def put_user(
    id: int,
    schema: UserRequest,
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.put_by_id(id=id, schema=schema)


@router.patch(
    "/{id}",
    response_model=UserOut,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
@inject
async def patch_user(
    id: int,
    schema: UserPasswordAdminRequest,
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await service.patch_password_by_id(user_id=id, schema=schema)


@router.delete(
    "/{id}",
    response_model=UserOut,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
@inject
async def delete_user(
    id: int,
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.delete_by_id(id=id)
