from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

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
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=None,
    exception_handlers={
        Exception: global_exception_handler,
        CoreException: core_exception_handler,
    },
    lifespan=lifespan,
    root_path=configs.PREFIX,
)


app.mount("/static", StaticFiles(directory="static"), name="static")
for routers in [v1_routers]:
    app.include_router(routers)
for middleware in [SessionMiddleware, LoggingMiddleware]:
    app.add_middleware(middleware)


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=f"{app.root_path}{app.openapi_url}",
        title=app.title,
        swagger_js_url=f"{app.root_path}/static/swagger-ui-bundle.js",
        swagger_css_url=f"{app.root_path}/static/swagger-ui.css",
        swagger_favicon_url=f"{app.root_path}/static/favicon.ico",
        oauth2_redirect_url=f"{app.root_path}/docs/oauth2-redirect",
        swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
    )


@app.get("/docs/oauth2-redirect", include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()
