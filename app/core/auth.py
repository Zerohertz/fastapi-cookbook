from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request
from fastapi.security import (
    HTTPBearer,
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordBearer,
)

from app.core.configs import configs, oauth_endpoints
from app.core.container import Container
from app.exceptions.auth import NotAuthenticated
from app.models.enums import Role
from app.schemas.auth import JwtAccessToken
from app.schemas.users import UserOut
from app.services.auth import AuthService


class JwtBearer(HTTPBearer):
    def __init__(
        self,
        *,
        bearerFormat: str | None = None,
        scheme_name: str | None = None,
        description: str | None = None,
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
    service: AuthService = Depends(Provide[Container.auth_service]),
) -> UserOut:
    schema = JwtAccessToken(access_token=access_token)
    return await service.verify(schema=schema)


UserAuthDeps = Depends(get_current_user)


async def get_admin_user(user: Annotated[UserOut, UserAuthDeps]) -> UserOut:
    if user.role != Role.ADMIN:
        raise NotAuthenticated
    return user


AdminAuthDeps = Depends(get_admin_user)

PasswordOAuthDeps = Depends(
    OAuth2PasswordBearer(
        tokenUrl=oauth_endpoints.PASSWORD_TOKEN, scheme_name="Password OAuth"
    )
)
GoogleOAuthDeps = Depends(
    OAuth2AuthorizationCodeBearer(
        authorizationUrl=f"https://accounts.google.com/o/oauth2/v2/auth?client_id={configs.GOOGLE_OAUTH_CLIENT_ID}",
        tokenUrl=oauth_endpoints.GOOGLE_TOKEN,
        refreshUrl=None,
        scheme_name="Google OAuth",
        scopes={
            "email": "Google Email",
            "profile": "Google Profile",
        },
    )
)
GitHubOAuthDeps = Depends(
    OAuth2AuthorizationCodeBearer(
        authorizationUrl=f"https://github.com/login/oauth/authorize?client_id={configs.GITHUB_OAUTH_CLIENT_ID}",
        tokenUrl=oauth_endpoints.GITHUB_TOKEN,
        # NOTE: https://github.com/Zerohertz/fastapi-cookbook/issues/33#issuecomment-2627994536
        refreshUrl=None,
        scheme_name="GitHub OAuth",
        scopes=None,
        # NOTE: &scope=repo,user
    )
)
