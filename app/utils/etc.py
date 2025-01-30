from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request

from app.core.container import Container
from app.models.users import User
from app.services.users import UserService


@inject
async def verify_cookie(
    request: Request,
    service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    access_token = request.cookies.get("access_token")
    user = await service.verify(access_token)
    return user
