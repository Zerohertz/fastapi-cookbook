import abc
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseSchemaRequest(BaseModel, abc.ABC):
    model_config = ConfigDict(from_attributes=True)


class BaseSchemaResponse(BaseModel, abc.ABC):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
