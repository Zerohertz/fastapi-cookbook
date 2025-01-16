from pydantic import AnyUrl, computed_field
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
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @computed_field
    @property
    def SQLMODEL_DATABASE_URI(self) -> AnyUrl:
        return MultiHostUrl.build(
            scheme=self.DB_TYPE,
            host=self.DB_HOST,
            port=self.DB_PORT,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            path=self.DB_NAME,
        )


configs = Configs()  # type: ignore
