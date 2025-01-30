from functools import wraps
from typing import Any, Callable, Coroutine, Type, TypeVar, cast

from fastapi import APIRouter, Response
from fastapi.types import DecoratedCallable
from loguru import logger
from pydantic import BaseModel

from app.schemas.responses import APIResponse

T = TypeVar("T", bound=BaseModel)


class CoreAPIRouter(APIRouter):
    def api_route(  # type: ignore
        self,
        path: str,
        *args,
        response_model: Type[T] | Type[Response],
        status_code: int,
        **kwargs,
    ) -> Callable[
        [DecoratedCallable],
        Callable[..., Coroutine[Any, Any, APIResponse[T] | Response]],
    ]:
        def decorator(
            func: DecoratedCallable,
        ) -> Callable[..., Coroutine[Any, Any, APIResponse[T] | Response]]:
            @wraps(func)
            async def success(
                *_args: tuple, **_kwargs: dict
            ) -> APIResponse[T] | Response:
                response: Any = await func(*_args, **_kwargs)
                if not isinstance(response, response_model):
                    logger.warning(f"{type(response)}: {response}")
                    raise TypeError
                if isinstance(response, BaseModel):
                    return APIResponse[T].success(
                        status=status_code, data=cast(T, response)
                    )
                return response

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
