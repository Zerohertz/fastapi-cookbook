from typing import Any, Generic, TypeVar, overload

from app.core.database import database
from app.models.base import BaseModel
from app.repositories.base import BaseRepository
from app.schemas.base import BaseSchemaRequest, BaseSchemaResponse

T = TypeVar("T", bound=BaseModel)


class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]) -> None:
        self.repository = repository

    @overload
    def mapper(self, data: BaseSchemaRequest) -> T: ...

    @overload
    def mapper(self, data: T) -> BaseSchemaResponse: ...

    def mapper(self, data: BaseSchemaRequest | T) -> T | BaseSchemaResponse:
        if isinstance(data, BaseSchemaRequest):
            return self.repository.model(**data.model_dump())
        return BaseSchemaResponse.model_validate(data)

    @database.transactional
    async def create(self, schema: BaseSchemaRequest) -> BaseSchemaResponse:
        entity = self.mapper(schema)
        entity = await self.repository.create(entity=entity)
        return self.mapper(entity)

    @database.transactional
    async def get_by_id(self, id: int) -> BaseSchemaResponse:
        entity = await self.repository.read_by_id(id=id)
        return self.mapper(entity)

    @database.transactional
    async def put_by_id(self, id: int, schema: BaseSchemaRequest) -> BaseSchemaResponse:
        entity = await self.repository.update_by_id(id=id, data=schema.model_dump())
        return self.mapper(entity)

    @database.transactional
    async def patch_by_id(
        self, id: int, schema: BaseSchemaRequest
    ) -> BaseSchemaResponse:
        entity = await self.repository.update_by_id(
            id=id, data=schema.model_dump(exclude_none=True)
        )
        return self.mapper(entity)

    @database.transactional
    async def patch_attr_by_id(
        self, id: int, attr: str, value: Any
    ) -> BaseSchemaResponse:
        entity = await self.repository.update_attr_by_id(
            id=id, column=attr, value=value
        )
        return self.mapper(entity)

    @database.transactional
    async def delete_by_id(self, id: int) -> BaseSchemaResponse:
        entity = await self.repository.delete_by_id(id=id)
        return self.mapper(entity)
