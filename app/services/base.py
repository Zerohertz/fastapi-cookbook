from typing import Any, Generic, TypeVar, overload

from app.core.database import database
from app.models.base import BaseModel
from app.repositories.base import BaseRepository
from app.schemas.base import BaseRequest, BaseResponse

T = TypeVar("T", bound=BaseModel)


class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]) -> None:
        self.repository = repository

    @overload
    def mapper(self, data: BaseRequest) -> T: ...

    @overload
    def mapper(self, data: T) -> BaseResponse: ...

    def mapper(self, data: BaseRequest | T) -> T | BaseResponse:
        if isinstance(data, BaseRequest):
            return self.repository.model(**data.model_dump())
        return BaseResponse.model_validate(data)

    @database.transactional
    async def create(self, schema: BaseRequest) -> BaseResponse:
        entity = self.mapper(schema)
        entity = await self.repository.create(entity=entity)
        return self.mapper(entity)

    @database.transactional
    async def get_by_id(self, id: int) -> BaseResponse:
        entity = await self.repository.read_by_id(id=id)
        return self.mapper(entity)

    @database.transactional
    async def put_by_id(self, id: int, schema: BaseRequest) -> BaseResponse:
        entity = await self.repository.update_by_id(id=id, data=schema.model_dump())
        return self.mapper(entity)

    @database.transactional
    async def patch_by_id(self, id: int, schema: BaseRequest) -> BaseResponse:
        entity = await self.repository.update_by_id(
            id=id, data=schema.model_dump(exclude_none=True)
        )
        return self.mapper(entity)

    @database.transactional
    async def patch_attr_by_id(self, id: int, attr: str, value: Any) -> BaseResponse:
        entity = await self.repository.update_attr_by_id(
            id=id, column=attr, value=value
        )
        return self.mapper(entity)

    @database.transactional
    async def delete_by_id(self, id: int) -> BaseResponse:
        entity = await self.repository.delete_by_id(id=id)
        return self.mapper(entity)
