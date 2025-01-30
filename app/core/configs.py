from enum import Enum
from typing import Optional

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class ENVIRONMENT(Enum):
    TEST = "TEST"
    DEV = "DEV"
    PROD = "PROD"


class Configs(BaseSettings):
    ENV: ENVIRONMENT

    # --------- APP SETTINGS --------- #
    PROJECT_NAME: str
    DESCRIPTION: str
    VERSION: str
    PREFIX: str
    TZ: str = "Asia/Seoul"

    # --------- DATABASE SETTINGS --------- #
    DB_TYPE: str
    DB_DRIVER: Optional[str]
    DB_HOST: Optional[str]
    DB_PORT: Optional[int] = 0
    DB_USER: Optional[str]
    DB_PASSWORD: Optional[str]
    DB_NAME: Optional[str]
    DB_ECHO: Optional[bool] = True
    DB_TABLE_CREATE: Optional[bool] = True

    # --------- AUTH SETTINGS --------- #
    GITHUB_OAUTH_CLIENT_ID: str
    GITHUB_OAUTH_CLIENT_SECRET: str
    # openssl rand -hex 32
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ADMIN_NAME: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

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
