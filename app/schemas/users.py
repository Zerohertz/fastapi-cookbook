from app.schemas.base import BaseSchemaRequest, BaseSchemaResponse


class UserCreateRequest(BaseSchemaRequest):
    name: str


class UserCreateResponse(BaseSchemaResponse):
    name: str
