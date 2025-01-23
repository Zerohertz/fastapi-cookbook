import time

import pytest
from fastapi.testclient import TestClient
from loguru import logger
from starlette import status

from app.core.configs import configs


@pytest.mark.run(order=1)
def test_create_user(sync_client: TestClient) -> None:
    """
    Post user route-create-1, route-create-2
    """
    for id in range(1, 3):
        name = f"route-create-{id}"
        response = sync_client.post(f"{configs.PREFIX}/v1/user", json={"name": name})
        logger.warning(response)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.run(order=2)
def test_get_user(sync_client: TestClient) -> None:
    """
    Get user create-1, create-2
    """
    for id in range(1, 3):
        name = f"route-create-{id}"
        response = sync_client.get(f"{configs.PREFIX}/v1/user/{id}")
        logger.warning(response)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        logger.warning(data)
        assert data["name"] == name


@pytest.mark.run(order=3)
def test_patch_user(sync_client: TestClient) -> None:
    """
    Patch user route-create-1 to route-patch
    """
    name = "route-patch"
    time.sleep(1)
    response = sync_client.patch(f"{configs.PREFIX}/v1/user/1", json={"name": name})
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    response = sync_client.get(f"{configs.PREFIX}/v1/user/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    logger.warning(data)
    assert data["name"] == name
    assert data["created_at"] != data["updated_at"]


@pytest.mark.run(order=3)
def test_put_user(sync_client: TestClient) -> None:
    """
    Put user route-create-2 to route-put
    """
    name = "route-put"
    time.sleep(1)
    response = sync_client.patch(f"{configs.PREFIX}/v1/user/2", json={"name": name})
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    response = sync_client.get(f"{configs.PREFIX}/v1/user/2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    logger.warning(data)
    assert data["name"] == name
    assert data["created_at"] != data["updated_at"]


@pytest.mark.run(order=4)
def test_delete_user(sync_client: TestClient) -> None:
    """
    Delete user route-patch, route-put
    """
    for id in range(1, 3):
        response = sync_client.delete(f"{configs.PREFIX}/v1/user/{id}")
        logger.warning(response)
        assert response.status_code == status.HTTP_200_OK
