from fastapi.testclient import TestClient

from app.core.configs import configs


def test_v1_jmy(client: TestClient) -> None:
    response = client.get(
        f"{configs.PREFIX}/v1/shields/jmy",
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("label") == "전문연구요원"
