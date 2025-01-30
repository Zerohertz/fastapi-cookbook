from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from starlette import status

from app.core.auth import AuthDeps
from app.core.container import Container
from app.core.router import CoreAPIRouter
from app.schemas.users import UserPatchRequest, UserRequest, UserResponse
from app.services.users import UserService

router = CoreAPIRouter(prefix="/user", tags=["user"])


@router.put(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
@inject
async def put_user(
    user: AuthDeps,
    schema: UserRequest,
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.put_by_id(id=user.id, schema=schema)


@router.patch(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
@inject
async def patch_user(
    user: AuthDeps,
    schema: UserPatchRequest,
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.patch_by_id(id=user.id, schema=schema)


@router.delete(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
@inject
async def delete_user(
    user: AuthDeps,
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.delete_by_id(id=user.id)
