from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    PROJECT_NAME: str
    PREFIX: str


configs = Configs()  # type: ignore
