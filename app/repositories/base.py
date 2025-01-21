from contextlib import AbstractContextManager
from typing import Any, Callable, Generic, Type, TypeVar

from loguru import logger
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload

from app.exceptions.database import EntityNotFound
from app.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(
        self,
        session: Callable[..., AbstractContextManager[Session]],
        model: Type[T],
    ) -> None:
        self.session = session
        self.model = model

    async def create(self, model: T) -> T:
        async with self.session() as session:
            session.add(model)
            await session.commit()
            await session.refresh(model)
        return model

    async def read_by_id(self, id: int, eager: bool = False) -> T:
        async with self.session() as session:
            query = select(self.model)
            if eager:
                for _eager in getattr(self.model, "eagers"):
                    query = query.options(joinedload(getattr(self.model, _eager)))
            query = query.filter(self.model.id == id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if not result:
                raise EntityNotFound
        return result

    async def update_by_id(self, id: int, model: dict) -> T:
        async with self.session() as session:
            query = select(self.model).filter(self.model.id == id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if not result:
                raise EntityNotFound
            logger.warning(result.updated_at)
            for key, value in model.items():
                setattr(result, key, value)
            await session.commit()
            await session.refresh(result)
            logger.warning(result.updated_at)
        return result

    async def update_attr_by_id(self, id: int, column: str, value: Any) -> T:
        async with self.session() as session:
            query = select(self.model).filter(self.model.id == id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if not result:
                raise EntityNotFound
            setattr(result, column, value)
            await session.commit()
        return result

    async def delete_by_id(self, id: int) -> T:
        async with self.session() as session:
            query = select(self.model).filter(self.model.id == id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if not result:
                raise EntityNotFound
            await session.delete(result)
            await session.commit()
        return result
