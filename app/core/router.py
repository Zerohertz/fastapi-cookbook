from functools import wraps
from typing import Awaitable, Callable

from fastapi import APIRouter
from fastapi.types import DecoratedCallable

from app.schemas.base import BaseSchema
from app.schemas.responses import APIResponse


class CoreAPIRouter(APIRouter):
    def api_route(
        self, path: str, *args, response_model: BaseSchema, status_code: int, **kwargs
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            @wraps(func)
            async def success(*_args: tuple, **_kwargs: dict) -> Awaitable:
                response = await func(*_args, **_kwargs)
                return APIResponse[response_model].success(
                    status=status_code, data=response
                )

            self.add_api_route(
                path,
                *args,
                success,
                response_model=APIResponse[response_model],
                status_code=status_code,
                **kwargs,
            )
            return success

        return decorator
