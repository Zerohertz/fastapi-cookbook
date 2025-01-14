from fastapi import FastAPI

from app.api.v1.routers import routers as v1_routers
from app.core.configs import configs
from app.core.lifespan import lifespan
from app.exceptions.handlers import global_exception_handler

app = FastAPI(
    title=configs.PROJECT_NAME,
    version="0.0.1",
    openapi_url=f"{configs.PREFIX}/openapi.json",
    docs_url=f"{configs.PREFIX}/docs",
    redoc_url=f"{configs.PREFIX}/redoc",
    exception_handlers={Exception: global_exception_handler},
    lifespan=lifespan,
)

for routers in [v1_routers]:
    app.include_router(routers, prefix=configs.PREFIX)
