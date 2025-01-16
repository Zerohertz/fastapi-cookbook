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
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str


configs = Configs()  # type: ignore
