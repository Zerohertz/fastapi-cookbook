from typing import Any, AsyncContextManager, Callable, Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.exceptions.database import EntityNotFound
from app.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(
        self,
        session: Callable[..., AsyncContextManager[AsyncSession]],
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
            _query = await session.execute(query)
            result = _query.scalar_one_or_none()
            if not result:
                raise EntityNotFound
        return result

    async def update_by_id(self, id: int, model: dict) -> T:
        async with self.session() as session:
            query = select(self.model).filter(self.model.id == id)
            _query = await session.execute(query)
            result = _query.scalar_one_or_none()
            if not result:
                raise EntityNotFound
            for key, value in model.items():
                setattr(result, key, value)
            await session.commit()
            await session.refresh(result)
        return result

    async def update_attr_by_id(self, id: int, column: str, value: Any) -> T:
        async with self.session() as session:
            query = select(self.model).filter(self.model.id == id)
            _query = await session.execute(query)
            result = _query.scalar_one_or_none()
            if not result:
                raise EntityNotFound
            setattr(result, column, value)
            await session.commit()
        return result

    async def delete_by_id(self, id: int) -> T:
        async with self.session() as session:
            query = select(self.model).filter(self.model.id == id)
            _query = await session.execute(query)
            result = _query.scalar_one_or_none()
            if not result:
                raise EntityNotFound
            await session.delete(result)
            await session.commit()
        return result
