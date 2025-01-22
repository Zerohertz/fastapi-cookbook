import time

from fastapi.testclient import TestClient
from loguru import logger
from starlette import status

from app.core.configs import configs


def test_create_user(client: TestClient) -> None:
    """
    Post user create-1, create-2
    """
    for id in range(1, 3):
        name = f"create-{id}"
        response = client.post(f"{configs.PREFIX}/v1/user", json={"name": name})
        logger.warning(response)
        assert response.status_code == status.HTTP_201_CREATED


def test_get_user(client: TestClient) -> None:
    """
    Get user create-1, create-2
    """
    for id in range(1, 3):
        name = f"create-{id}"
        response = client.get(f"{configs.PREFIX}/v1/user/{id}")
        logger.warning(response)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        logger.warning(data)
        assert data["name"] == name


def test_patch_user(client: TestClient) -> None:
    """
    Patch user create-1
    """
    name = "patch"
    time.sleep(1)
    response = client.patch(f"{configs.PREFIX}/v1/user/1", json={"name": name})
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    response = client.get(f"{configs.PREFIX}/v1/user/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    logger.warning(data)
    assert data["name"] == name
    assert data["created_at"] != data["updated_at"]


def test_put_user(client: TestClient) -> None:
    """
    Put user create-1
    """
    name = "put"
    time.sleep(1)
    response = client.patch(f"{configs.PREFIX}/v1/user/2", json={"name": name})
    logger.warning(response)
    assert response.status_code == status.HTTP_200_OK
    response = client.get(f"{configs.PREFIX}/v1/user/2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    logger.warning(data)
    assert data["name"] == name
    assert data["created_at"] != data["updated_at"]
