import pytest
from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient
from loguru import logger

from app.core.configs import configs
from app.schemas.auth import PasswordOAuthReigsterRequest
from app.schemas.users import UserPatchRequest, UserRequest
from app.tests.api.v1.test_auth import MockUser, register_and_log_in

fake = Faker()


def log_in_admin(sync_client: TestClient) -> tuple[MockUser, str]:
    admin_user = MockUser(
        sync_client=sync_client,
        request=PasswordOAuthReigsterRequest(
            grant_type="password",
            username=configs.ADMIN_EMAIL,
            password=configs.ADMIN_PASSWORD,
            name=configs.ADMIN_NAME,
        ),
    )
    access_token = admin_user.log_in()
    return admin_user, access_token


def test_get_user_name(sync_client: TestClient) -> None:
    admin_user, admin_access_token = log_in_admin(sync_client)
    mock_user, user_access_token = register_and_log_in(sync_client)
    response = sync_client.get(
        f"{configs.PREFIX}/v1/user/",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert isinstance(data, list)
    assert 1 < len(data)
    response = sync_client.get(
        f"{configs.PREFIX}/v1/user/",
        headers={"Authorization": f"Bearer {user_access_token}"},
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = sync_client.get(
        f"{configs.PREFIX}/v1/user/1",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    logger.warning(response)
    data = response.json()["data"]
    assert data["id"] == 1
    assert data["name"] == configs.ADMIN_NAME
    assert data["email"] == configs.ADMIN_EMAIL
    assert data["oauth"] == "password"
    assert response.status_code == status.HTTP_200_OK
    response = sync_client.get(
        f"{configs.PREFIX}/v1/user/1",
        headers={"Authorization": f"Bearer {user_access_token}"},
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_patch_user_password(sync_client: TestClient) -> None:
    admin_user, admin_access_token = log_in_admin(sync_client)
    mock_user, user_access_token = register_and_log_in(sync_client)
    request = UserPatchRequest(password=fake.password())
    response = sync_client.patch(
        f"{configs.PREFIX}/v1/user/{mock_user.get_me(user_access_token)}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
        json=request.model_dump(),
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    with pytest.raises(AssertionError):
        mock_user.log_in()
    if request.password is None:
        raise ValueError
    mock_user.request.password = request.password
    mock_user.log_in()


def test_put_user(sync_client: TestClient) -> None:
    admin_user, admin_access_token = log_in_admin(sync_client)
    mock_user, user_access_token = register_and_log_in(sync_client)
    request = UserRequest(name=fake.name(), email=fake.email())
    response = sync_client.put(
        f"{configs.PREFIX}/v1/user/{mock_user.get_me(user_access_token)}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
        json=request.model_dump(),
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert data["name"] != mock_user.request.name
    assert data["email"] != mock_user.request.username
    assert data["name"] == request.name
    assert data["email"] == request.email


def test_delete_user(sync_client: TestClient) -> None:
    admin_user, admin_access_token = log_in_admin(sync_client)
    mock_user, user_access_token = register_and_log_in(sync_client)
    response = sync_client.delete(
        f"{configs.PREFIX}/v1/user/{mock_user.get_me(user_access_token)}",
        headers={"Authorization": f"Bearer {admin_access_token}"},
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert data["name"] == mock_user.request.name
    assert data["email"] == mock_user.request.username
    with pytest.raises(AssertionError):
        mock_user.log_in()
