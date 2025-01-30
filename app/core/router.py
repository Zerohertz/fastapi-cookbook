from functools import wraps
from typing import Any, Callable, Coroutine, Type, TypeVar

from fastapi import APIRouter, Response
from fastapi.types import DecoratedCallable
from loguru import logger
from pydantic import BaseModel

from app.exceptions.router import RouterTypeError
from app.schemas.responses import APIResponse

T = TypeVar("T", bound=BaseModel)


class CoreAPIRouter(APIRouter):
    def api_route(  # type: ignore
        self,
        path: str,
        *,
        response_model: Type[T],
        response_class: Type[Response],
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
            async def endpoint(
                *_args: tuple, **_kwargs: dict
            ) -> APIResponse[T] | Response:
                response: Any = await func(*_args, **_kwargs)
                if isinstance(response, response_class):
                    return response
                if isinstance(response, tuple):
                    # NOTE: 아래 두 변수는 차후 사용 시 추가
                    # media_type: str | None = None,
                    # background: BackgroundTask | None = None,
                    content, headers = response
                    return response_class(
                        content=APIResponse[response_model]  # type: ignore[valid-type]
                        .success(
                            status=status_code,
                            data=content,
                        )
                        .model_dump(mode="json"),
                        status_code=status_code,
                        headers=headers,
                    )
                if isinstance(response, (BaseModel, list)):
                    return response_class(
                        content=APIResponse[response_model]  # type: ignore[valid-type]
                        .success(
                            status=status_code,
                            data=response,
                        )
                        .model_dump(mode="json"),
                        status_code=status_code,
                    )
                logger.error(f"{type(response)}: {response}")
                raise RouterTypeError

            if response_model is None:
                self.add_api_route(
                    path=path,
                    endpoint=endpoint,
                    response_model=response_model,
                    response_class=response_class,
                    status_code=status_code,
                    **kwargs,
                )
            else:
                self.add_api_route(
                    path=path,
                    endpoint=endpoint,
                    response_model=APIResponse[response_model],  # type: ignore[valid-type]
                    response_class=response_class,
                    status_code=status_code,
                    **kwargs,
                )
            return endpoint

        return decorator
