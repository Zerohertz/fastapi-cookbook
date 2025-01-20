from contextlib import AbstractContextManager
from typing import Any, Callable, Generic, Type, TypeVar

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

    def create(self, model: T) -> T:
        with self.session() as session:
            session.add(model)
            session.commit()
            session.refresh(model)
        return model

    def read_by_id(self, id: int, eager: bool = False) -> T:
        with self.session() as session:
            query = session.query(self.model)
            if eager:
                for _eager in getattr(self.model, "eagers"):
                    query = query.options(joinedload(getattr(self.model, _eager)))
            result = query.filter(self.model.id == id).first()
            if not result:
                raise EntityNotFound
        return result

    def update_by_id(self, id: int, model: dict) -> T:
        with self.session() as session:
            session.query(self.model).filter(self.model.id == id).update(model)
            session.commit()
            result = session.query(self.model).filter(self.model.id == id).first()
            if not result:
                raise EntityNotFound
        return result

    def update_attr_by_id(self, id: int, column: str, value: Any) -> T:
        with self.session() as session:
            session.query(self.model).filter(self.model.id == id).update(
                {column: value}
            )
            session.commit()
            result = session.query(self.model).filter(self.model.id == id).first()
            if not result:
                raise EntityNotFound
        return result

    def delete_by_id(self, id: int) -> T:
        with self.session() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            if not query:
                raise EntityNotFound
            session.delete(query)
            session.commit()
        return query
