from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.schemas.responses import APIResponse


def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"{request=}, {exc=}")
    name = exc.__class__.__name__
    return JSONResponse(
        content=APIResponse.error(
            status=HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"""[{name}] {" ".join(exc.args)}""",
        ).model_dump(mode="json"),
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


def business_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"{request=}, {exc=}")
    name = exc.__class__.__name__
    return JSONResponse(
        content=APIResponse.error(
            status=exc.status, message=f"[{name}] {exc.message}"
        ).model_dump(mode="json"),
        status_code=exc.status,
    )
