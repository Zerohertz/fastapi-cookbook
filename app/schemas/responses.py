from datetime import datetime
from typing import Generic, Optional, Sequence, TypeVar

import pytz
from pydantic import BaseModel

from app.core.configs import configs

T = TypeVar("T", bound=BaseModel)


class APIResponse(BaseModel, Generic[T]):
    """
    Generic을 통해 어떤 type이 될지 모르는 출력 data의 type hint를 지정한다.

    Examples:

        class User(BaseModel):
            name: str

        >>> print(APIResponse[User].success(status=200, data=User(id=1, created_at=datetime.now(), updated_at=datetime.now(), name="123")).model_dump_json())
        {"status":200,"message":"The request has been successfully processed.","data":{"id":1,"created_at":"2025-01-20T13:23:40.132620","updated_at":"2025-01-20T13:23:40.132627","name":"123"},"timestamp":"2025-01-20T13:23:40.132646"}
        >>> print(APIResponse.success(status=200, data=User(id=1, created_at=datetime.now(), updated_at=datetime.now(), name="123")).model_dump_json())
        {"status":200,"message":"The request has been successfully processed.","data":{"id":1,"created_at":"2025-01-20T13:24:19.341066","updated_at":"2025-01-20T13:24:19.341072","name":"123"},"timestamp":"2025-01-20T13:24:19.341090"}

        >>> print(APIResponse[User].error(status=404, message="fail").model_dump_json())
        {"status":404,"message":"fail","data":null,"timestamp":"2025-01-20T13:25:51.258688"}
        >>> print(APIResponse.error(status=404, message="fail").model_dump_json())
        {"status":404,"message":"fail","data":null,"timestamp":"2025-01-20T13:25:57.358318"}
    """

    status: int
    message: str
    data: Optional[T | Sequence[T]] = None
    timestamp: datetime

    @classmethod
    def success(cls, *, status: int, data: T | Sequence[T]) -> "APIResponse[T]":
        return cls(
            status=status,
            message="The request has been successfully processed.",
            data=data,
            timestamp=datetime.now().astimezone(pytz.timezone(configs.TZ)),
        )

    @classmethod
    def error(cls, *, status: int, message: str) -> "APIResponse[T]":
        return cls(
            status=status,
            message=message,
            data=None,
            timestamp=datetime.now().astimezone(pytz.timezone(configs.TZ)),
        )
