from fastapi.testclient import TestClient
from loguru import logger

from app.core.configs import configs


def test_v1_user(client: TestClient) -> None:
    user_ids = list(range(5))
    for user_id in user_ids:
        try:
            response = client.get(
                f"{configs.PREFIX}/v1/user?user_id={user_id}",
            )
        except Exception:
            pass
        if user_id == 0:
            assert response.status_code == 200
        else:
            content = response.json()
            logger.error(content)
