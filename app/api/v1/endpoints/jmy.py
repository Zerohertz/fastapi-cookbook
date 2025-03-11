from typing import Literal

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Query, status
from fastapi.responses import ORJSONResponse

from app.core.auth import (
    GitHubOAuthDeps,
    GoogleOAuthDeps,
    PasswordOAuthDeps,
)
from app.core.container import Container
from app.core.router import CoreAPIRouter
from app.schemas.jmy import JmyCompanyOut, JmyPageResponse
from app.services.jmy import JmyService

router = CoreAPIRouter(prefix="/jmy", tags=["jmy"])


@router.get(
    "",
    response_model=JmyPageResponse,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[PasswordOAuthDeps, GoogleOAuthDeps, GitHubOAuthDeps],
    summary="",
    description="",
)
@inject
async def get_jmy_page(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=10, le=100),
    sort_by: Literal["old", "new"] = "old",
    filter_by: Literal["ms", "phd", "all"] = "all",
    service: JmyService = Depends(Provide[Container.jmy_service]),
):
    return await service.get_page(
        page=page, size=size, sort_by=sort_by, filter_by=filter_by
    )


@router.get(
    "/{id}",
    response_model=JmyCompanyOut,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[PasswordOAuthDeps, GoogleOAuthDeps, GitHubOAuthDeps],
    summary="",
    description="",
)
@inject
async def get_jmy_by_id(
    id: int,
    service: JmyService = Depends(Provide[Container.jmy_service]),
):
    return await service.get_by_id(id=id)
