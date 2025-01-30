from contextvars import Token

import pytest
from faker import Faker
from loguru import logger

from app.core.container import Container
from app.exceptions.database import DatabaseException, EntityNotFound
from app.models.enums import OAuthProvider, Role
from app.schemas.users import UserIn, UserPatchRequest, UserRequest

fake = Faker()


def get_mock_user() -> UserIn:
    return UserIn(
        name=fake.name(),
        email=fake.email(),
        password=fake.password(),
        role=Role.USER,
        oauth=OAuthProvider.PASSWORD,
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_create_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    user_service = container.user_service()
    for id in range(10):
        schema = get_mock_user()
        user = await user_service.create(schema=schema)
        assert user.name == schema.name
        assert user.email == schema.email
    # TODO: DatabaseException
    with pytest.raises(DatabaseException):
        user = await user_service.create(schema=schema)


@pytest.mark.asyncio(loop_scope="function")
async def test_get_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    user_service = container.user_service()
    for id in range(10, 20):
        schema = get_mock_user()
        user = await user_service.create(schema=schema)
        user = await user_service.get_by_id(id=user.id)
        assert user.name == schema.name
        assert user.email == schema.email
    with pytest.raises(EntityNotFound):
        user = await user_service.get_by_id(id=99999)


@pytest.mark.asyncio(loop_scope="function")
async def test_put_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    user_service = container.user_service()
    for id in range(20, 30):
        schema = get_mock_user()
        user = await user_service.create(schema=schema)
        schema.name = fake.name()
        schema.email = fake.email()
        user = await user_service.put_by_id(
            id=user.id, schema=UserRequest.model_validate(schema.model_dump())
        )
        assert user.name == schema.name
        assert user.email == schema.email
    with pytest.raises(EntityNotFound):
        user = await user_service.put_by_id(
            id=99999, schema=UserRequest(name=fake.name(), email=fake.email())
        )


@pytest.mark.asyncio(loop_scope="function")
async def test_patch_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    user_service = container.user_service()
    for id in range(30, 40):
        schema = get_mock_user()
        user = await user_service.create(schema=schema)
        schema.email = fake.email()
        schema.password = fake.password()
        user = await user_service.patch_by_id(
            id=user.id, schema=UserPatchRequest.model_validate(schema.model_dump())
        )
        assert user.name == schema.name
        assert user.email == schema.email
        _name = fake.name()
        user = await user_service.patch_attr_by_id(id=user.id, attr="name", value=_name)
        assert user.name == _name
    with pytest.raises(EntityNotFound):
        user = await user_service.patch_by_id(
            id=99999,
            schema=UserPatchRequest(name=fake.name(), email=fake.email()),
        )
    with pytest.raises(EntityNotFound):
        user = await user_service.patch_attr_by_id(
            id=99999, attr="name", value=fake.name()
        )


@pytest.mark.asyncio(loop_scope="function")
async def test_delete_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    user_service = container.user_service()
    for _ in range(0, 10):
        schema = get_mock_user()
        user = await user_service.create(schema=schema)
        user = await user_service.delete_by_id(id=user.id)
    with pytest.raises(EntityNotFound):
        user = await user_service.delete_by_id(id=99999)
