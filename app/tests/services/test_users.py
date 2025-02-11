from contextvars import Token

import pytest
from faker import Faker
from loguru import logger

from app.core.container import Container
from app.exceptions.database import DatabaseException, EntityNotFound
from app.models.enums import Role
from app.schemas.users import UserIn, UserRequest

pytestmark = pytest.mark.anyio
fake = Faker()


def get_mock_user() -> UserIn:
    return UserIn(
        name=fake.name(),
        email=fake.email(),
        role=Role.USER,
    )


async def test_create_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    user_service = container.user_service()
    for _ in range(10):
        schema = get_mock_user()
        user = await user_service.create(schema=schema)
        assert user.name == schema.name
        assert user.email == schema.email
    # TODO: DatabaseException
    with pytest.raises(DatabaseException):
        user = await user_service.create(schema=schema)


async def test_get_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    user_service = container.user_service()
    for _ in range(10):
        schema = get_mock_user()
        user = await user_service.create(schema=schema)
        user = await user_service.get_by_id(id=user.id)
        assert user.name == schema.name
        assert user.email == schema.email
    with pytest.raises(EntityNotFound):
        user = await user_service.get_by_id(id=99999)


async def test_put_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    user_service = container.user_service()
    for _ in range(10):
        schema = get_mock_user()
        user = await user_service.create(schema=schema)
        schema.name = fake.name()
        user = await user_service.put_by_id(
            id=user.id, schema=UserRequest.model_validate(schema.model_dump())
        )
        assert user.name == schema.name
    with pytest.raises(EntityNotFound):
        user = await user_service.put_by_id(
            id=99999, schema=UserRequest(name=fake.name())
        )


async def test_delete_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    user_service = container.user_service()
    for _ in range(10):
        schema = get_mock_user()
        user = await user_service.create(schema=schema)
        user = await user_service.delete_by_id(id=user.id)
    with pytest.raises(EntityNotFound):
        user = await user_service.delete_by_id(id=99999)
