import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=unused-argument
    logging.getLogger("uvicorn.error").setLevel(logging.CRITICAL)
    logger.remove()
    logger.add(sys.stderr, colorize=True)
    yield
