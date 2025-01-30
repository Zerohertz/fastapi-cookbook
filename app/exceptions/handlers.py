from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger

from app.exceptions.base import CoreException
from app.schemas.responses import APIResponse


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"{request=}, {exc=}")
    name = exc.__class__.__name__
    return JSONResponse(
        content=APIResponse.error(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"""[{name}] {" ".join(exc.args)}""",
        ).model_dump(mode="json"),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def core_exception_handler(
    request: Request, exc: CoreException  # pylint: disable=unused-argument
) -> JSONResponse:
    logger.error(exc)
    return JSONResponse(
        content=APIResponse.error(status=exc.status, message=repr(exc)).model_dump(
            mode="json"
        ),
        status_code=exc.status,
    )
