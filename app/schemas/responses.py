from datetime import datetime
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class APIResponse(BaseModel, Generic[T]):
    """
    Generic을 통해 어떤 type이 될지 모르는 출력 data의 type hint를 지정한다.

    Examples:

        class User(BaseModel):
            name: str

        >>> print(APIResponse[User].success(status=200, data=User(name="123")))
        status=200 message='The request has been successfully processed.' data=User(name='123') timestamp=datetime.datetime(2025, 1, 8, 22, 46, 32, 337336)
        >>> print(APIResponse.success(status=200, data=User(name="123")))
        status=200 message='The request has been successfully processed.' data=User(name='123') timestamp=datetime.datetime(2025, 1, 8, 22, 46, 32, 337384)
        >>> print(APIResponse.error(status=404, message="fail"))
        status=404 message='fail' data=None timestamp=datetime.datetime(2025, 1, 8, 22, 46, 32, 337411)
    """

    status: int
    message: str
    data: Optional[T] = None
    timestamp: datetime

    @classmethod
    def success(cls, *, status: int, data: T) -> "APIResponse[T]":
        return cls(
            status=status,
            message="The request has been successfully processed.",
            data=data,
            timestamp=datetime.now(),
        )

    @classmethod
    def error(cls, *, status: int, message: str) -> "APIResponse[T]":
        return cls(status=status, message=message, data=None, timestamp=datetime.now())


if __name__ == "__main__":

    class User(BaseModel):
        name: str

    print(APIResponse[User].success(status=200, data=User(name="123")))
    print(APIResponse.success(status=200, data=User(name="123")))
    print(APIResponse.error(status=404, message="fail"))
