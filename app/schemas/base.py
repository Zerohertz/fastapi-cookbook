import abc
from datetime import datetime

import pytz
from pydantic import BaseModel, ConfigDict, model_validator
from typing_extensions import Self

from app.core.configs import configs


class BaseRequest(BaseModel, abc.ABC):
    model_config = ConfigDict(from_attributes=True)


class BaseResponse(BaseModel, abc.ABC):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

    @model_validator(mode="after")
    def set_timezone(self) -> Self:
        self.created_at = self.created_at.astimezone(pytz.timezone(configs.TZ))
        self.updated_at = self.updated_at.astimezone(pytz.timezone(configs.TZ))
        return self
