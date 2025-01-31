from functools import wraps
from typing import Any, Callable, Coroutine, Type, TypeVar

from fastapi import APIRouter, Response
from fastapi.types import DecoratedCallable
from loguru import logger
from pydantic import BaseModel

from app.exceptions.router import RouterTypeError
from app.schemas.base import BaseResponse
from app.schemas.responses import APIResponse

T = TypeVar("T", bound=BaseModel)


class CoreAPIRouter(APIRouter):
    def api_route(  # type: ignore[override]
        self,
        path: str,
        *,
        response_model: None | Type[BaseModel] | Type[T],
        response_class: Type[Response],
        status_code: int,
        **kwargs,
    ) -> Callable[
        [DecoratedCallable],
        Callable[..., Coroutine[Any, Any, Response]],
    ]:
        def decorator(
            func: DecoratedCallable,
        ) -> Callable[..., Coroutine[Any, Any, Response]]:
            @wraps(func)
            async def endpoint(*_args: tuple, **_kwargs: dict) -> Response:
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
                if isinstance(response, (BaseResponse, list)):
                    return response_class(
                        content=APIResponse[response_model]  # type: ignore[valid-type]
                        .success(
                            status=status_code,
                            data=response,
                        )
                        .model_dump(mode="json"),
                        status_code=status_code,
                    )
                if isinstance(response, BaseModel):
                    return response_class(
                        content=response.model_dump(mode="json"),
                        status_code=status_code,
                    )
                logger.error(f"{type(response)=}, {response=}")
                raise RouterTypeError

            _response_model: None | Type[BaseModel] | Type[APIResponse[T]]
            if response_model is not None and (
                (
                    hasattr(response_model, "__origin__")
                    and response_model.__origin__ is list
                )
                or issubclass(response_model, BaseResponse)
            ):
                _response_model = APIResponse[response_model]  # type: ignore[valid-type]
            elif response_model is None or issubclass(response_model, BaseModel):
                _response_model = response_model
            else:
                raise RouterTypeError
            self.add_api_route(
                path=path,
                endpoint=endpoint,
                response_model=_response_model,
                response_class=response_class,
                status_code=status_code,
                **kwargs,
            )
            return endpoint

        return decorator
