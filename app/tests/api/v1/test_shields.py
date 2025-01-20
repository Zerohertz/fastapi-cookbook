from fastapi.testclient import TestClient
from starlette import status

from app.core.configs import configs


def test_jmy(client: TestClient) -> None:
    response = client.get(
        f"{configs.PREFIX}/v1/shields/jmy",
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data.get("label") == "전문연구요원"
