from fastapi import FastAPI

from app.api.v1.routers import routers as v1_routers
from app.core.configs import configs
from app.core.lifespan import lifespan
from app.core.middlewares import LoggingMiddleware
from app.exceptions.base import BusinessException
from app.exceptions.handlers import business_exception_handler, global_exception_handler

app = FastAPI(
    title=configs.PROJECT_NAME,
    version="0.0.1",
    openapi_url=f"{configs.PREFIX}/openapi.json",
    docs_url=f"{configs.PREFIX}/docs",
    redoc_url=f"{configs.PREFIX}/redoc",
    exception_handlers={
        Exception: global_exception_handler,
        BusinessException: business_exception_handler,
    },
    lifespan=lifespan,
)

for routers in [v1_routers]:
    app.include_router(routers, prefix=configs.PREFIX)
for middleware in [LoggingMiddleware]:
    app.add_middleware(middleware)
