from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from starlette import status

from app.core.container import Container
from app.core.router import CoreAPIRouter
from app.schemas.users import UserCreateRequest, UserCreateResponse
from app.services.users import UserService

router = CoreAPIRouter(prefix="/user", tags=["user"])


@router.post(
    "",
    response_model=UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="",
    description="",
)
@inject
async def create_user(
    user: UserCreateRequest,
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.create(user)


@router.get(
    "/{id}",
    response_model=UserCreateResponse,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
@inject
async def get_user(
    id: int,
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.get_by_id(id)


@router.put(
    "/{id}",
    response_model=UserCreateResponse,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
@inject
async def put_user(
    id: int,
    user: UserCreateRequest,
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.put_by_id(id=id, schema=user)


@router.patch(
    "/{id}",
    response_model=UserCreateResponse,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
@inject
async def patch_user(
    id: int,
    user: UserCreateRequest,
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.patch_by_id(id=id, schema=user)


@router.delete(
    "/{id}",
    response_model=UserCreateResponse,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
@inject
async def delete_user(
    id: int,
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.delete_by_id(id)
