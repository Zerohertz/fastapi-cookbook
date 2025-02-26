from enum import Enum
from typing import Annotated, List

from pydantic import computed_field, field_validator
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, NoDecode


class ENVIRONMENT(Enum):
    TEST = "TEST"
    DEV = "DEV"
    PROD = "PROD"


class Configs(BaseSettings):
    ENV: ENVIRONMENT = ENVIRONMENT.TEST

    # --------- APP SETTINGS --------- #
    PROJECT_NAME: str
    DESCRIPTION: str
    VERSION: str
    BACKEND_URL: str
    FRONTEND_URL: str
    PREFIX: str
    TZ: str = "Asia/Seoul"

    # --------- DATABASE SETTINGS --------- #
    DB_TYPE: str
    DB_DRIVER: str
    DB_HOST: str
    DB_PORT: int = 0
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_ECHO: bool = True
    DB_TABLE_CREATE: bool = True

    # --------- AUTH SETTINGS --------- #
    ALLOW_ORIGINS: Annotated[List[str], NoDecode] = []

    @field_validator("ALLOW_ORIGINS", mode="before")
    @classmethod
    def allow_origins(cls, value: str) -> List[str]:
        if value:
            return value.split(",")
        return []

    # openssl rand -hex 32
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    TOKEN_URLSAFE_NBYTES: int = 128

    ADMIN_NAME: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    GOOGLE_OAUTH_CLIENT_ID: str
    GOOGLE_OAUTH_CLIENT_SECRET: str
    GITHUB_OAUTH_CLIENT_ID: str
    GITHUB_OAUTH_CLIENT_SECRET: str

    @property
    def DB_SCHEME(self) -> str:
        if self.DB_DRIVER:
            return f"{self.DB_TYPE}+{self.DB_DRIVER}"
        return self.DB_TYPE

    @computed_field  # type: ignore[prop-decorator]
    @property
    def DATABASE_URI(self) -> str:
        if self.DB_TYPE == "sqlite" and self.DB_PORT == 0:
            if self.DB_DRIVER:
                return f"{self.DB_TYPE}+{self.DB_DRIVER}:///{self.DB_NAME}"
            return f"{self.DB_TYPE}:///{self.DB_NAME}"
        return str(
            MultiHostUrl.build(
                scheme=self.DB_SCHEME,
                host=self.DB_HOST,
                port=self.DB_PORT,
                username=self.DB_USER,
                password=self.DB_PASSWORD,
                path=self.DB_NAME,
            )
        )


configs = Configs()  # type: ignore[call-arg]


class OAuthEndpoints(BaseSettings):
    PASSWORD_TOKEN: str = f"{configs.PREFIX}/v1/auth/password/token"
    GOOGLE_TOKEN: str = f"{configs.PREFIX}/v1/auth/google/token"
    GITHUB_TOKEN: str = f"{configs.PREFIX}/v1/auth/github/token"

    GOOGLE_CALLBACK: str = f"{configs.PREFIX}/v1/auth/google/callback"
    GITHUB_CALLBACK: str = f"{configs.PREFIX}/v1/auth/github/callback"


oauth_endpoints = OAuthEndpoints()
