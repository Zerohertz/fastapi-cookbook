from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Response, status
from fastapi.responses import RedirectResponse

from app.core.auth import AuthDeps
from app.core.configs import configs
from app.core.container import Container
from app.core.router import CoreAPIRouter
from app.schemas.auth import JwtAccessToken, JwtRefreshToken, JwtToken
from app.schemas.users import (
    UserOut,
    UserPasswordRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.services.users import UserService

router = CoreAPIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/refresh",
    response_model=JwtAccessToken,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
@inject
async def post_refresh_token(
    token: JwtRefreshToken,
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.refresh(token)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register with password",
    description="",
)
@inject
async def register_password(
    request: UserRegisterRequest,
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.register(request)


@router.post(
    "/login",
    response_model=JwtToken,
    status_code=status.HTTP_200_OK,
    summary="Log in with password",
    description="",
)
@inject
async def log_in_password(
    request: UserPasswordRequest,
    service: UserService = Depends(Provide[Container.user_service]),
):
    return await service.log_in_password(schema=request)


@router.get(
    "/oauth/login/github",
    response_model=Response,
    status_code=status.HTTP_302_FOUND,
    summary="Log in with GitHub OAuth",
    description="GitHub OAuth를 위해 redirection",
)
async def log_in_github():
    # NOTE: &scope=repo,user
    # TODO: APIResponse (related: #24)
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={configs.GITHUB_OAUTH_CLIENT_ID}"
    )


@router.get(
    "/oauth/callback/github",
    response_model=JwtToken,
    status_code=status.HTTP_200_OK,
    summary="Callback for GitHub OAuth",
    description="GitHub OAuth에 의해 redirection될 endpoint",
    include_in_schema=False,
)
@inject
async def callback_github(
    code: str,
    service: UserService = Depends(Provide[Container.user_service]),
):
    """
    # NOTE: Cookie 방식으로 JWT token 사용 시
    response.set_cookie(
        key="access_token", value=jwt_token.access_token, httponly=True, secure=True
    )
    response.set_cookie(
        key="refresh_token", value=jwt_token.refresh_token, httponly=True, secure=True
    )
    """
    return await service.log_in_github(code=code)


@router.get(
    "/me",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="",
    description="",
)
async def get_me(user: AuthDeps):
    return user
