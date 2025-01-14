import logging
import sys
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.utils.logging import remove_handler


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=unused-argument
    remove_handler(logging.getLogger("uvicorn.access"))
    remove_handler(logging.getLogger("uvicorn.error"))
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <bg #800a0a>"
        + time.tzname[0]
        + "</bg #800a0a> | <level>{level: <8}</level> | <fg #800a0a>{name}</fg #800a0a>:<fg #800a0a>{function}</fg #800a0a>:<fg #800a0a>{line}</fg #800a0a> - <level>{message}</level>",
        colorize=True,
    )
    # logging.getLogger("uvicorn.access").addHandler(LoguruHandler())
    # logging.getLogger("uvicorn.error").addHandler(LoguruHandler())
    yield
