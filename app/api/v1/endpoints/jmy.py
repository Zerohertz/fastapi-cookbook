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
from app.schemas.jmy import JmyCompanyOut
from app.services.jmy import JmyService

router = CoreAPIRouter(
    prefix="/jmy",
    tags=["jmy"],
    dependencies=[AdminAuthDeps, PasswordOAuthDeps, GoogleOAuthDeps, GitHubOAuthDeps],
)


@router.get(
    "/{id}",
    response_model=JmyCompanyOut,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
@inject
async def get_jmy(
    id: int,
    service: JmyService = Depends(Provide[Container.jmy_service]),
):
    return await service.get_by_id(id=id)
