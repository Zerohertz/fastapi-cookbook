import secrets
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Form, Request, status
from fastapi.responses import ORJSONResponse, RedirectResponse

from app.core.auth import (
    GitHubOAuthDeps,
    GoogleOAuthDeps,
    PasswordOAuthDeps,
    UserAuthDeps,
)
from app.core.configs import configs, oauth_endpoints
from app.core.container import Container
from app.core.router import CoreAPIRouter
from app.exceptions.auth import GitHubOAuthFailed
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
    response_class=ORJSONResponse,
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
    "/password/register",
    response_model=UserResponse,
    response_class=ORJSONResponse,
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
    "/password/token",
    response_model=JwtToken,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtain an access token via password authentication",
    description="- Authenticate using an email and password to obtain an access token.</br>\n"
    "- This token can be used for subsequent API requests.",
)
@inject
async def token_password(
    # NOTE: OAuth2PasswordRequestForm
    request: Annotated[PasswordOAuthRequest, Form(...)],
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await service.token_password(schema=request)


@router.get(
    "/google/login",
    response_model=None,
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    summary="",
    description="",
)
async def log_in_google():
    state = secrets.token_urlsafe(nbytes=configs.TOKEN_URLSAFE_NBYTES)
    response = RedirectResponse(
        url="https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={configs.GOOGLE_OAUTH_CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={configs.BACKEND_URL}{oauth_endpoints.GOOGLE_CALLBACK}"
        f"&state={state}"
        "&scope=email profile",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
    response.set_cookie(key="oauth_google_state", value=state, httponly=True)
    return response


@router.get(
    "/google/callback",
    response_model=JwtToken,
    response_class=RedirectResponse,
    status_code=status.HTTP_302_FOUND,
    summary="Obtain an access token via Google OAuth",
    description="- Authenticate using Google OAuth and receive an access token.<br/>\n"
    "- The client must provide an authorization code obtained from Google.",
)
@inject
async def callback_google(
    code: str,
    state: str,
    request: Request,
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    # NOTE: /?code=***&state=***
    # /?state=***&code=***&scope=***&authuser=***&prompt=***

    if state != request.cookies.get("oauth_google_state"):
        raise GitHubOAuthFailed
    jwt_token = await service.token_google(
        GoogleOAuthRequest(
            grant_type="authorization_code",
            code=code,
            redirect_uri=f"{configs.BACKEND_URL}{oauth_endpoints.GOOGLE_CALLBACK}",
        )
    )
    return RedirectResponse(
        url=f"{configs.FRONTEND_URL}/login"
        f"?access_token={jwt_token.access_token}"
        f"&refresh_token={jwt_token.refresh_token}"
        f"&token_type={jwt_token.token_type}"
        f"&expires_in={jwt_token.expires_in}",
        status_code=status.HTTP_302_FOUND,
    )


@router.post(
    "/google/token",
    response_model=JwtToken,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtain an access token via Google OAuth",
    description="- Authenticate using Google OAuth and receive an access token.<br/>\n"
    "- The client must provide an authorization code obtained from Google.",
)
@inject
async def token_google(
    request: Annotated[GoogleOAuthRequest, Form()],
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await service.token_google(request)


@router.get(
    "/github/login",
    response_model=None,
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    summary="",
    description="",
)
async def log_in_github():
    state = secrets.token_urlsafe(nbytes=configs.TOKEN_URLSAFE_NBYTES)
    response = RedirectResponse(
        url="https://github.com/login/oauth/authorize?"
        f"client_id={configs.GITHUB_OAUTH_CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={configs.BACKEND_URL}{oauth_endpoints.GITHUB_CALLBACK}"
        f"&state={state}",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
    response.set_cookie(key="oauth_github_state", value=state, httponly=True)
    return response


@router.get(
    "/github/callback",
    response_model=JwtToken,
    response_class=RedirectResponse,
    status_code=status.HTTP_302_FOUND,
    summary="Obtain an access token via GitHub OAuth",
    description="- Authenticate using GitHub OAuth and receive an access token.<br/>\n"
    "- The client must provide an authorization code obtained from GitHub.",
)
@inject
async def callback_github(
    code: str,
    state: str,
    request: Request,
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    # NOTE: /?code=***&state=***
    if state != request.cookies.get("oauth_github_state"):
        raise GitHubOAuthFailed
    jwt_token = await service.token_github(
        GitHubOAuthRequest(
            grant_type="authorization_code", code=code, redirect_uri=configs.BACKEND_URL
        )
    )
    return RedirectResponse(
        url=f"{configs.FRONTEND_URL}/login"
        f"?access_token={jwt_token.access_token}"
        f"&refresh_token={jwt_token.refresh_token}"
        f"&token_type={jwt_token.token_type}"
        f"&expires_in={jwt_token.expires_in}",
        status_code=status.HTTP_302_FOUND,
    )


@router.post(
    "/github/token",
    response_model=JwtToken,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtain an access token via GitHub OAuth",
    description="- Authenticate using GitHub OAuth and receive an access token.<br/>\n"
    "- The client must provide an authorization code obtained from GitHub.",
)
@inject
async def token_github(
    request: Annotated[GitHubOAuthRequest, Form()],
    service: AuthService = Depends(Provide[Container.auth_service]),
):
    return await service.token_github(request)


@router.get(
    "/me",
    response_model=UserOut,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[PasswordOAuthDeps, GoogleOAuthDeps, GitHubOAuthDeps],
    summary="Retrieve the current authenticated user's information",
    description="- Returns the authenticated user's details based on the provided access token.</br>\n"
    "- Requires a valid token obtained via password authentication or GitHub OAuth.",
)
async def get_me(user: Annotated[UserOut, UserAuthDeps]):
    return user
