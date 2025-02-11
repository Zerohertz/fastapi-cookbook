from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Form, status
from fastapi.responses import JSONResponse

from app.core.auth import (
    GitHubOAuthDeps,
    GoogleOAuthDeps,
    PasswordOAuthDeps,
    UserAuthDeps,
)
from app.core.container import Container
from app.core.router import CoreAPIRouter
from app.schemas.auth import (
    GitHubOAuthRequest,
    GoogleOAuthRequest,
    JwtToken,
    PasswordOAuthReigsterRequest,
    PasswordOAuthRequest,
    RefreshOAuthRequest,
)
from app.schemas.users import UserOut, UserResponse
from app.services.auth import AuthService

router = CoreAPIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/refresh",
    response_model=JwtToken,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description="- Refresh the access token using a valid refresh token.</br>\n"
    "- If the refresh token is invalid or expired, authentication will fail.",
)
@inject
async def refresh(
    request: Annotated[RefreshOAuthRequest, Form(...)],
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await service.refresh(request)


@router.post(
    "/register/password",
    response_model=UserResponse,
    response_class=JSONResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new account with a password",
    description="- Create a new user account using an email and password.</br>\n"
    "- The provided credentials will be used for authentication.",
)
@inject
async def register_password(
    request: Annotated[PasswordOAuthReigsterRequest, Form(...)],
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await service.register(request)


@router.post(
    "/token/password",
    response_model=JwtToken,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtain an access token via password authentication",
    description="- Authenticate using an email and password to obtain an access token.</br>\n"
    "- This token can be used for subsequent API requests.",
)
@inject
async def log_in_password(
    # NOTE: OAuth2PasswordRequestForm
    request: Annotated[PasswordOAuthRequest, Form(...)],
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await service.log_in_password(schema=request)


@router.post(
    "/token/google",
    response_model=JwtToken,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtain an access token via Google OAuth",
    description="- Authenticate using Google OAuth and receive an access token.<br/>\n"
    "- The client must provide an authorization code obtained from Google.",
)
@inject
async def log_in_google(
    request: Annotated[GoogleOAuthRequest, Form()],
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await service.log_in_google(request)


@router.post(
    "/token/github",
    response_model=JwtToken,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtain an access token via GitHub OAuth",
    description="- Authenticate using GitHub OAuth and receive an access token.<br/>\n"
    "- The client must provide an authorization code obtained from GitHub.",
)
@inject
async def log_in_github(
    request: Annotated[GitHubOAuthRequest, Form()],
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await service.log_in_github(request)


@router.get(
    "/me",
    response_model=UserOut,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[PasswordOAuthDeps, GoogleOAuthDeps, GitHubOAuthDeps],
    summary="Retrieve the current authenticated user's information",
    description="- Returns the authenticated user's details based on the provided access token.</br>\n"
    "- Requires a valid token obtained via password authentication or GitHub OAuth.",
)
async def get_me(user: Annotated[UserOut, UserAuthDeps]):
    return user
