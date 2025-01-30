import pytest
from faker import Faker
from fastapi.testclient import TestClient
from loguru import logger
from starlette import status

from app.core.configs import configs
from app.schemas.users import UserPasswordRequest, UserPatchRequest, UserRequest
from app.tests.api.v1.test_auth import log_in, register_and_login

fake = Faker()


def test_patch_user_name(sync_client: TestClient) -> None:
    schema, access_token = register_and_login(sync_client)
    request = UserPatchRequest(name=fake.name())
    response = sync_client.patch(
        f"{configs.PREFIX}/v1/user/",
        headers={"Authorization": f"Bearer {access_token}"},
        json=request.model_dump(),
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert data["name"] != schema.name
    assert data["name"] == request.name


def test_patch_user_password(sync_client: TestClient) -> None:
    schema, access_token = register_and_login(sync_client)
    request = UserPatchRequest(password=fake.password())
    response = sync_client.patch(
        f"{configs.PREFIX}/v1/user/",
        headers={"Authorization": f"Bearer {access_token}"},
        json=request.model_dump(),
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    with pytest.raises(AssertionError):
        log_in(sync_client, UserPasswordRequest.model_validate(schema.model_dump()))
    if request.password is None:
        raise ValueError
    log_in(
        sync_client, UserPasswordRequest(email=schema.email, password=request.password)
    )


def test_put_user(sync_client: TestClient) -> None:
    schema, access_token = register_and_login(sync_client)
    request = UserRequest(name=fake.name(), email=fake.email())
    response = sync_client.put(
        f"{configs.PREFIX}/v1/user/",
        headers={"Authorization": f"Bearer {access_token}"},
        json=request.model_dump(),
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert data["name"] != schema.name
    assert data["email"] != schema.email
    assert data["name"] == request.name
    assert data["email"] == request.email


def test_delete_user(sync_client: TestClient) -> None:
    schema, access_token = register_and_login(sync_client)
    response = sync_client.delete(
        f"{configs.PREFIX}/v1/user/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert data["name"] == schema.name
    assert data["email"] == schema.email
