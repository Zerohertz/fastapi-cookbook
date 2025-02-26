from fastapi import Request, status
from fastapi.responses import ORJSONResponse
from loguru import logger

from app.exceptions.base import CoreException
from app.schemas.responses import APIResponse


async def global_exception_handler(request: Request, exc: Exception) -> ORJSONResponse:
    logger.exception(f"{request=}, {exc=}")
    name = exc.__class__.__name__
    return ORJSONResponse(
        content=APIResponse.error(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"""[{name}] {" ".join(exc.args)}""",
        ).model_dump(mode="json"),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def core_exception_handler(
    request: Request, exc: CoreException  # pylint: disable=unused-argument
) -> ORJSONResponse:
    logger.exception(exc)
    return ORJSONResponse(
        content=APIResponse.error(status=exc.status, message=repr(exc)).model_dump(
            mode="json"
        ),
        status_code=exc.status,
    )
