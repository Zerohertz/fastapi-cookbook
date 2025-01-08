import abc
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseSchema(BaseModel, abc.ABC):
    """
    https://docs.pydantic.dev/latest/concepts/models/#abstract-base-classes
    """

    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
