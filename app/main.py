import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from loguru import logger

from app.api.v1.routers import routers as v1_routers
from app.core.configs import configs
from app.core.decorators import exception


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.getLogger("uvicorn.error").setLevel(logging.CRITICAL)
    logger.remove()
    logger.add(sys.stderr, colorize=True)
    yield


app = FastAPI(
    title=configs.PROJECT_NAME,
    openapi_url=f"{configs.PREFIX}/openapi.json",
    docs_url=f"{configs.PREFIX}/docs",
    redoc_url=f"{configs.PREFIX}/redoc",
    version="0.0.1",
    lifespan=lifespan,
)
for routers in [v1_routers]:
    app.include_router(routers, prefix=configs.PREFIX)


@app.exception_handler(Exception)
@exception
def global_exception_handler(request: Request, exc: Exception) -> None:
    logger.error(f"{request=}, {exc=}")
