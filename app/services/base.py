from typing import Any, Generic, TypeVar, overload

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

    def create(self, schema: BaseSchemaRequest) -> BaseSchemaResponse:
        model = self.mapper(schema)
        model = self.repository.create(model=model)
        return self.mapper(model)

    def get_by_id(self, id: int) -> BaseSchemaResponse:
        model = self.repository.read_by_id(id=id)
        return self.mapper(model)

    def put_by_id(self, id: int, schema: BaseSchemaRequest) -> BaseSchemaResponse:
        model = self.repository.update_by_id(id=id, model=schema.model_dump())
        return self.mapper(model)

    def patch_by_id(self, id: int, schema: BaseSchemaRequest) -> BaseSchemaResponse:
        model = self.repository.update_by_id(
            id=id, model=schema.model_dump(exclude_none=True)
        )
        return self.mapper(model)

    def patch_attr_by_id(self, id: int, attr: str, value: Any) -> BaseSchemaResponse:
        model = self.repository.update_attr_by_id(id=id, column=attr, value=value)
        return self.mapper(model)

    def delete_by_id(self, id: int) -> BaseSchemaResponse:
        model = self.repository.delete_by_id(id=id)
        return self.mapper(model)