import pytest
from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient
from loguru import logger

from app.core.configs import configs
from app.schemas.users import UserPasswordRequest, UserRequest
from app.tests.api.v1.test_auth import register_and_log_in

fake = Faker()


def test_put_user(sync_client: TestClient) -> None:
    mock_user, access_token = register_and_log_in(sync_client)
    request = UserRequest(name=fake.name())
    response = sync_client.put(
        f"{configs.PREFIX}/v1/user",
        headers={"Authorization": f"Bearer {access_token}"},
        json=request.model_dump(),
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert data["name"] != mock_user.request.name
    assert data["name"] == request.name


def test_patch_user(sync_client: TestClient) -> None:
    mock_user, access_token = register_and_log_in(sync_client)
    request = UserPasswordRequest(
        password_old=mock_user.request.password, password_new=fake.password()
    )
    response = sync_client.patch(
        f"{configs.PREFIX}/v1/user",
        headers={"Authorization": f"Bearer {access_token}"},
        json=request.model_dump(),
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    with pytest.raises(AssertionError):
        mock_user.log_in()
    mock_user.request.password = request.password_new
    mock_user.log_in()


def test_delete_user(sync_client: TestClient) -> None:
    mock_user, access_token = register_and_log_in(sync_client)
    response = sync_client.delete(
        f"{configs.PREFIX}/v1/user",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert data["name"] == mock_user.request.name
    assert data["email"] == mock_user.request.username
