from functools import wraps

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.exceptions.base import BusinessException
from app.schemas.responses import ApiResponse


def exception(func):
    @wraps(func)
    def wrapper(request: Request, exc: Exception):
        func(request, exc)
        name = exc.__class__.__name__
        if isinstance(exc, BusinessException):
            return JSONResponse(
                content=ApiResponse.error(
                    status=exc.status, message=f"[{name}] {exc.message}"
                ).model_dump(mode="json"),
                status_code=exc.status,
            )
        return JSONResponse(
            content=ApiResponse.error(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"""[{name}] {" ".join(exc.args)}""",
            ).model_dump(mode="json"),
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return wrapper
