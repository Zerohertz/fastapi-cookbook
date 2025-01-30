from typing import Annotated, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.container import Container
from app.exceptions.auth import NotAuthenticated
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

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        try:
            authorization = await super().__call__(request)
            return authorization.credentials
        except HTTPException:
            raise NotAuthenticated


jwt_bearer = JwtBearer()


@inject
async def get_current_user(
    access_token: Annotated[HTTPAuthorizationCredentials, Depends(jwt_bearer)],
    service: UserService = Depends(Provide[Container.user_service]),
) -> UserOut:
    token = JwtAccessToken(access_token=access_token)
    return await service.verify(token=token)


AuthDeps = Annotated[UserOut, Depends(get_current_user)]
