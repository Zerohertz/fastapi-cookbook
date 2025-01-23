# import time
#
# import pytest
# from fastapi.testclient import TestClient
# from httpx import put
# from loguru import logger
# from starlette import status
#
# from app.core.configs import configs
#
#
# def test_crud_user(sync_client: TestClient) -> None:
#     ids = create_user(sync_client)
#     get_user(sync_client, ids)
#     patch_user(sync_client, ids)
#     put_user(sync_client, ids)
#     delete_user(sync_client, ids)
#
#
# def create_user(sync_client: TestClient) -> list[tuple[int]]:
#     ids = []
#     for id in range(30):
#         name = f"routes-create-{id}"
#         response = sync_client.post(f"{configs.PREFIX}/v1/user", json={"name": name})
#         logger.warning(response)
#         assert response.status_code == status.HTTP_201_CREATED
#         data = response.json()["data"]
#         ids.append((data["id"], id))
#     return ids
#
#
# def get_user(sync_client: TestClient, ids: list[tuple[int]]) -> None:
#     for pk, id in ids:
#         name = f"routes-create-{id}"
#         response = sync_client.get(f"{configs.PREFIX}/v1/user/{pk}")
#         logger.warning(response)
#         assert response.status_code == status.HTTP_200_OK
#         data = response.json()["data"]
#         logger.warning(data)
#         assert data["name"] == name
#
#
# def patch_user(sync_client: TestClient, ids: list[tuple[int]]) -> None:
#     for pk, id in ids[:5]:
#         name = f"routes-patch-{id}"
#         time.sleep(1)
#         response = sync_client.patch(
#             f"{configs.PREFIX}/v1/user/{pk}", json={"name": name}
#         )
#         logger.warning(response)
#         assert response.status_code == status.HTTP_200_OK
#         response = sync_client.get(f"{configs.PREFIX}/v1/user/{pk}")
#         assert response.status_code == status.HTTP_200_OK
#         data = response.json()["data"]
#         logger.warning(data)
#         assert data["name"] == name
#         assert data["created_at"] != data["updated_at"]
#
#
# def put_user(sync_client: TestClient, ids: list[tuple[int]]) -> None:
#     for pk, id in ids[:5]:
#         name = f"routes-put-{id}"
#         time.sleep(1)
#         response = sync_client.put(
#             f"{configs.PREFIX}/v1/user/{pk}", json={"name": name}
#         )
#         logger.warning(response)
#         assert response.status_code == status.HTTP_200_OK
#         response = sync_client.get(f"{configs.PREFIX}/v1/user/{pk}")
#         assert response.status_code == status.HTTP_200_OK
#         data = response.json()["data"]
#         logger.warning(data)
#         assert data["name"] == name
#         assert data["created_at"] != data["updated_at"]
#
#
# def delete_user(sync_client: TestClient, ids: list[tuple[int]]) -> None:
#     for pk, _ in ids:
#         response = sync_client.delete(f"{configs.PREFIX}/v1/user/{pk}")
#         logger.warning(response)
#         assert response.status_code == status.HTTP_200_OK
