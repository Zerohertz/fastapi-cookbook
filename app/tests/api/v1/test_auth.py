from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient
from loguru import logger

from app.core.configs import configs
from app.models.enums import OAuthProvider, Role
from app.schemas.users import UserPasswordRequest, UserRegisterRequest

fake = Faker()


def test_register_and_login(sync_client: TestClient):
    for _ in range(5):
        request, access_token = register_and_login(sync_client)
        get_me(sync_client, request, access_token)
    response = sync_client.post(
        f"{configs.PREFIX}/v1/auth/register/",
        json=request.model_dump(),
    )
    assert response.status_code == 409


def get_mock_request() -> UserRegisterRequest:
    return UserRegisterRequest(
        name=fake.name(), email=fake.email(), password=fake.password()
    )


def register_and_login(sync_client: TestClient) -> tuple[UserRegisterRequest, str]:
    request = get_mock_request()
    register(sync_client, request)
    access_token = log_in(
        sync_client, UserPasswordRequest.model_validate(request.model_dump())
    )
    return request, access_token


def register(sync_client: TestClient, request: UserRegisterRequest) -> None:
    response = sync_client.post(
        f"{configs.PREFIX}/v1/auth/register/",
        json=request.model_dump(),
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()["data"]
    assert request.name == data["name"]
    assert request.email == data["email"]


def log_in(sync_client: TestClient, request: UserPasswordRequest) -> str:
    response = sync_client.post(
        f"{configs.PREFIX}/v1/auth/login/", json=request.model_dump()
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    return data["access_token"]


def get_me(sync_client: TestClient, request: UserRegisterRequest, access_token: str):
    logger.warning(access_token)
    response = sync_client.get(
        f"{configs.PREFIX}/v1/auth/me/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    logger.warning(response)
    logger.warning(response.json())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert data["oauth"] == OAuthProvider.PASSWORD.value
    assert data["role"] == Role.USER.value
    assert data["name"] == request.name
    assert data["email"] == request.email
    assert data["password"] != request.password
