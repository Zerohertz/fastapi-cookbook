from typing import Any, Generic, TypeVar, overload

from app.core.database import database
from app.models.base import BaseModel
from app.repositories.base import BaseRepository
from app.schemas.base import BaseRequest, BaseResponse

Model = TypeVar("Model", bound=BaseModel)
Request = TypeVar("Request", bound=BaseRequest)
Response = TypeVar("Response", bound=BaseResponse)


class BaseMapper(Generic[Model, Request, Response]):
    def __init__(self, *, model: type[Model], schema: type[Response]) -> None:
        self.model = model
        self.schema = schema

    @overload
    def __call__(self, data: Request) -> Model: ...

    @overload
    def __call__(self, data: Model) -> Response: ...

    def __call__(self, data: Request | Model) -> Model | Response:
        if isinstance(data, BaseRequest):
            return self.model(**data.model_dump())
        return self.schema.model_validate(data)


class BaseService(Generic[Model, Request, Response]):
    def __init__(
        self, repository: BaseRepository[Model], schema: type[Response]
    ) -> None:
        self.repository = repository
        self.mapper = BaseMapper[Model, Request, Response](
            model=self.repository.model, schema=schema
        )

    @database.transactional
    async def create(self, schema: Request) -> Response:
        entity = self.mapper(schema)
        entity = await self.repository.create(entity=entity)
        return self.mapper(entity)

    async def get_by_id(self, id: int, eager: bool = False) -> Response:
        entity = await self.repository.read_by_id(id=id, eager=eager)
        return self.mapper(entity)

    @database.transactional
    async def put_by_id(self, id: int, schema: Request) -> Response:
        entity = await self.repository.update_by_id(id=id, data=schema.model_dump())
        return self.mapper(entity)

    @database.transactional
    async def patch_by_id(self, id: int, schema: Request) -> Response:
        entity = await self.repository.update_by_id(
            id=id, data=schema.model_dump(exclude_none=True)
        )
        return self.mapper(entity)

    @database.transactional
    async def patch_attr_by_id(self, id: int, attr: str, value: Any) -> Response:
        entity = await self.repository.update_attr_by_id(
            id=id, column=attr, value=value
        )
        return self.mapper(entity)

    @database.transactional
    async def delete_by_id(self, id: int, eager: bool = False) -> Response:
        entity = await self.repository.delete_by_id(id=id, eager=eager)
        return self.mapper(entity)
