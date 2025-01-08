from pydantic_settings import BaseSettings


class Configs(BaseSettings):
    PROJECT_NAME: str = "💨 Zerohertz's FastAPI Boilerplate 💨"
    PREFIX: str = "/api"


configs = Configs()
