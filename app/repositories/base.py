from typing import Any, Generic, Type, TypeVar

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.core.database import database
from app.exceptions.database import EntityAlreadyExists, EntityNotFound
from app.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(
        self,
        model: Type[T],
    ) -> None:
        self.model = model

    async def create(self, model: T) -> T:
        session = database.scoped_session()
        session.add(model)
        try:
            await session.flush()
        except IntegrityError:
            raise EntityAlreadyExists
        await session.refresh(model)
        return model

    async def read_by_id(self, id: int, eager: bool = False) -> T:
        query = select(self.model)
        if eager:
            for _eager in getattr(self.model, "eagers"):
                query = query.options(joinedload(getattr(self.model, _eager)))
        query = query.filter(self.model.id == id)
        session = database.scoped_session()
        _query = await session.execute(query)
        result = _query.scalar_one_or_none()
        if not result:
            raise EntityNotFound
        return result

    async def update_by_id(self, id: int, model: dict) -> T:
        query = select(self.model).filter(self.model.id == id)
        session = database.scoped_session()
        _query = await session.execute(query)
        result = _query.scalar_one_or_none()
        if not result:
            raise EntityNotFound
        for key, value in model.items():
            setattr(result, key, value)
        try:
            await session.flush()
        except IntegrityError:
            raise EntityAlreadyExists
        return result

    async def update_attr_by_id(self, id: int, column: str, value: Any) -> T:
        query = select(self.model).filter(self.model.id == id)
        session = database.scoped_session()
        _query = await session.execute(query)
        result = _query.scalar_one_or_none()
        if not result:
            raise EntityNotFound
        setattr(result, column, value)
        try:
            await session.flush()
        except IntegrityError:
            raise EntityAlreadyExists
        return result

    async def delete_by_id(self, id: int) -> T:
        query = select(self.model).filter(self.model.id == id)
        session = database.scoped_session()
        _query = await session.execute(query)
        result = _query.scalar_one_or_none()
        if not result:
            raise EntityNotFound
        await session.delete(result)
        return result
