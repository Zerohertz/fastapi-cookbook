from fastapi import Request
from loguru import logger

from app.core.decorators import exception


@exception
def global_exception_handler(request: Request, exc: Exception) -> None:
    logger.error(f"{request=}, {exc=}")
