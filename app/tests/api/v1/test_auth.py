from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient
from loguru import logger

from app.core.configs import configs
from app.models.enums import OAuthProvider, Role
from app.schemas.auth import PasswordOAuthReigsterRequest, PasswordOAuthRequest

fake = Faker()


def get_mock_request() -> PasswordOAuthReigsterRequest:
    return PasswordOAuthReigsterRequest(
        grant_type=OAuthProvider.PASSWORD,
        username=fake.email(),
        password=fake.password(),
        name=fake.name(),
    )


class MockUser:
    def __init__(
        self,
        sync_client: TestClient,
        request: PasswordOAuthReigsterRequest | None = None,
    ) -> None:
        self.client = sync_client
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        if request:
            self.request = request
        else:
            self.request = get_mock_request()

    def register(self) -> None:
        response = self.client.post(
            f"{configs.PREFIX}/v1/auth/register/password/",
            headers=self.headers,
            data=self.request.model_dump(),
        )
        logger.warning(response)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()["data"]
        assert data["name"] == self.request.name
        assert data["email"] == self.request.username

    def log_in(self) -> str:
        request = PasswordOAuthRequest.model_validate(self.request.model_dump())
        response = self.client.post(
            f"{configs.PREFIX}/v1/auth/token/password/",
            headers=self.headers,
            data=request.model_dump(),
        )
        logger.warning(response)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "token_type" in data
        assert "expires_in" in data
        return data["access_token"]

    def get_me(self, access_token: str) -> int:
        logger.warning(access_token)
        response = self.client.get(
            f"{configs.PREFIX}/v1/auth/me/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        logger.warning(response)
        logger.warning(response.json())
        assert response.status_code == status.HTTP_200_OK
        data = response.json()["data"]
        assert data["role"] == Role.USER.value
        assert data["name"] == self.request.name
        assert data["email"] == self.request.username
        return data["id"]
        assert data["oauth"][0]["provider"] == OAuthProvider.PASSWORD.value
        assert data["oauth"][0]["provider"] != self.request.password


def register_and_log_in(sync_client: TestClient) -> tuple[MockUser, str]:
    mock_user = MockUser(sync_client=sync_client)
    mock_user.register()
    access_token = mock_user.log_in()
    return mock_user, access_token


def test_register_and_log_in(sync_client: TestClient):
    for _ in range(5):
        mock_user, access_token = register_and_log_in(sync_client)
        mock_user.get_me(access_token)
    response = sync_client.post(
        f"{configs.PREFIX}/v1/auth/register/password/",
        headers=mock_user.headers,
        data=mock_user.request.model_dump(),
    )
    assert response.status_code == 409
