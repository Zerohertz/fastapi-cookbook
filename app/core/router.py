from functools import wraps
from typing import Any, Awaitable, Callable, Coroutine, Type, TypeVar

from fastapi import APIRouter
from fastapi.types import DecoratedCallable

from app.schemas.base import BaseSchema
from app.schemas.responses import APIResponse

T = TypeVar("T", bound=BaseSchema)


class CoreAPIRouter(APIRouter):
    def api_route(  # type: ignore
        self,
        path: str,
        *args,
        response_model: Type[T],
        status_code: int,
        **kwargs,
    ) -> Callable[
        [DecoratedCallable], Callable[..., Coroutine[Any, Any, APIResponse[T]]]
    ]:
        def decorator(
            func: DecoratedCallable,
        ) -> Callable[..., Coroutine[Any, Any, APIResponse[T]]]:
            @wraps(func)
            async def success(*_args: tuple, **_kwargs: dict) -> APIResponse[T]:
                response: T = await func(*_args, **_kwargs)
                return APIResponse[T].success(status=status_code, data=response)

            self.add_api_route(
                path,
                success,
                *args,
                response_model=APIResponse[T],
                status_code=status_code,
                **kwargs,
            )
            return success

        return decorator
