from typing import Any, Generic, Type, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.core.database import database
from app.exceptions.database import (
    DatabaseException,
    EntityAlreadyExists,
    EntityNotFound,
)
from app.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(
        self,
        model: Type[T],
    ) -> None:
        self.model = model

    def _eager(self, *, stmt: Select) -> Select:
        for _eager in getattr(self.model, "eagers"):
            stmt = stmt.options(joinedload(getattr(self.model, _eager)))
        return stmt

    async def create(self, entity: T) -> T:
        session = database.scoped_session()
        session.add(entity)
        try:
            await session.flush()
        except IntegrityError as error:
            # TODO: DB engine에 따라서 오류가 천차만별
            # message 기반으로 하기는 어려울 것으로 보임
            raise DatabaseException from error
        await session.refresh(instance=entity)
        return entity

    async def read_by_id(self, id: int, eager: bool = False) -> T:
        stmt = select(self.model)
        if eager:
            stmt = self._eager(stmt=stmt)
        stmt = stmt.where(self.model.id == id)
        session = database.scoped_session()
        result = await session.execute(stmt)
        entity = result.scalar_one_or_none()
        if not entity:
            raise EntityNotFound
        return entity

    async def update_by_id(self, id: int, data: dict) -> T:
        stmt = select(self.model).where(self.model.id == id)
        session = database.scoped_session()
        result = await session.execute(stmt)
        entity = result.scalar_one_or_none()
        if not entity:
            raise EntityNotFound
        for key, value in data.items():
            setattr(entity, key, value)
        try:
            await session.flush()
        except IntegrityError as error:
            raise EntityAlreadyExists from error
        await session.refresh(entity)
        return entity

    async def update_attr_by_id(self, id: int, column: str, value: Any) -> T:
        stmt = select(self.model).where(self.model.id == id)
        session = database.scoped_session()
        result = await session.execute(stmt)
        entity = result.scalar_one_or_none()
        if not entity:
            raise EntityNotFound
        setattr(entity, column, value)
        try:
            await session.flush()
        except IntegrityError as error:
            raise EntityAlreadyExists from error
        await session.refresh(entity)
        return entity

    async def delete_by_id(self, id: int, eager: bool = False) -> T:
        stmt = select(self.model).where(self.model.id == id)
        if eager:
            stmt = self._eager(stmt=stmt)
        session = database.scoped_session()
        result = await session.execute(stmt)
        entity = result.scalar_one_or_none()
        if not entity:
            raise EntityNotFound
        await session.delete(entity)
        return entity
