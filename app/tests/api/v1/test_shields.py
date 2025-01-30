from fastapi import status
from fastapi.testclient import TestClient

from app.core.configs import configs


def test_jmy(sync_client: TestClient) -> None:
    response = sync_client.get(
        f"{configs.PREFIX}/v1/shields/jmy",
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data.get("label") == "전문연구요원"
