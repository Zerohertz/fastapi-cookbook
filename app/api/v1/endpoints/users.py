from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.responses import JSONResponse

from app.core.auth import GitHubOAuthDeps, PasswordOAuthDeps, UserAuthDeps
from app.core.container import Container
from app.core.router import CoreAPIRouter
from app.schemas.users import UserOut, UserPatchRequest, UserRequest, UserResponse
from app.services.users import UserService

router = CoreAPIRouter(prefix="/user", tags=["user"])


@router.put(
    "/",
    response_model=UserResponse,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[PasswordOAuthDeps, GitHubOAuthDeps],
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
    "/",
    response_model=UserResponse,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[PasswordOAuthDeps, GitHubOAuthDeps],
    summary="",
    description="",
)
@inject
async def patch_user(
    schema: UserPatchRequest,
    user: Annotated[UserOut, UserAuthDeps],
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.patch_by_id(id=user.id, schema=schema)


@router.delete(
    "/",
    response_model=UserResponse,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[PasswordOAuthDeps, GitHubOAuthDeps],
    summary="",
    description="",
)
@inject
async def delete_user(
    user: Annotated[UserOut, UserAuthDeps],
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.delete_by_id(id=user.id)
