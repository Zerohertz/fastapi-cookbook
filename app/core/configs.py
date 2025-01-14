from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    PROJECT_NAME: str
    DESCRIPTION: str
    PREFIX: str


configs = Configs()  # type: ignore
