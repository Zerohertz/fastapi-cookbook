from fastapi import FastAPI

from app.api.v1.routers import routers as v1_routers
from app.core.configs import configs
from app.core.lifespan import lifespan
from app.core.middlewares import LoggingMiddleware, SessionMiddleware
from app.exceptions.base import CoreException
from app.exceptions.handlers import core_exception_handler, global_exception_handler

app = FastAPI(
    title=configs.PROJECT_NAME,
    summary="",
    description=configs.DESCRIPTION,
    version=configs.VERSION,
    openapi_url=f"{configs.PREFIX}/openapi.json",
    docs_url=f"{configs.PREFIX}/docs",
    redoc_url=None,
    exception_handlers={
        Exception: global_exception_handler,
        CoreException: core_exception_handler,
    },
    lifespan=lifespan,
)

for routers in [v1_routers]:
    app.include_router(routers, prefix=configs.PREFIX)
for middleware in [SessionMiddleware, LoggingMiddleware]:
    app.add_middleware(middleware)
