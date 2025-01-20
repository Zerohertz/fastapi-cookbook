from typing import Optional

from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    # --------- APP SETTINGS --------- #
    PROJECT_NAME: str
    DESCRIPTION: str
    VERSION: str
    PREFIX: str

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

    @property
    def DB_SCHEME(self) -> str:
        if self.DB_DRIVER:
            return f"{self.DB_TYPE}+{self.DB_DRIVER}"
        return self.DB_TYPE

    @computed_field  # type: ignore[prop-decorator]
    @property
    def DATABASE_URI(self) -> str:
        if self.DB_TYPE == "sqlite" and self.DB_PORT == 0:
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


configs = Configs()  # type: ignore
