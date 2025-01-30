from contextvars import Token

import pytest
from faker import Faker
from loguru import logger

from app.core.container import Container
from app.exceptions.database import EntityAlreadyExists, EntityNotFound
from app.schemas.users import UserIn, UserRequest

fake = Faker()


@pytest.mark.asyncio(loop_scope="function")
async def test_create_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    user_service = container.user_service()
    for id in range(10):
        _name = fake.name()
        _email = fake.email()
        user = await user_service.create(
            schema=UserIn(name=_name, email=_email, oauth="test")
        )
        assert user.name == _name
        assert user.email == _email
    with pytest.raises(EntityAlreadyExists):
        user = await user_service.create(
            schema=UserIn(name=_name, email=_email, oauth="test")
        )


@pytest.mark.asyncio(loop_scope="function")
async def test_get_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    user_service = container.user_service()
    for id in range(10, 20):
        _name = fake.name()
        _email = fake.email()
        user = await user_service.create(
            schema=UserIn(name=_name, email=_email, oauth="test")
        )
        user = await user_service.get_by_id(id=user.id)
        assert user.name == _name
    with pytest.raises(EntityNotFound):
        user = await user_service.get_by_id(id=99999)


@pytest.mark.asyncio(loop_scope="function")
async def test_put_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    user_service = container.user_service()
    for id in range(20, 30):
        _name = fake.name()
        _email = fake.email()
        user = await user_service.create(
            schema=UserIn(name=_name, email=_email, oauth="test")
        )
        _name = fake.name()
        _email = fake.email()
        user = await user_service.put_by_id(
            id=user.id, schema=UserRequest(name=_name, email=_email)
        )
        assert user.name == _name
    with pytest.raises(EntityNotFound):
        user = await user_service.put_by_id(
            id=99999, schema=UserRequest(name=fake.name(), email=fake.email())
        )


@pytest.mark.asyncio(loop_scope="function")
async def test_patch_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    user_service = container.user_service()
    for id in range(30, 40):
        _name = fake.name()
        _email = fake.email()
        user = await user_service.create(
            schema=UserIn(name=_name, email=_email, oauth="test")
        )
        _name = fake.name()
        _email = fake.email()
        user = await user_service.patch_by_id(
            id=user.id, schema=UserRequest(name=_name, email=_email)
        )
        assert user.name == _name
        _name = fake.name()
        user = await user_service.patch_attr_by_id(id=user.id, attr="name", value=_name)
        assert user.name == _name
    with pytest.raises(EntityNotFound):
        user = await user_service.patch_by_id(
            id=99999, schema=UserRequest(name=fake.name(), email=fake.email())
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
        user = await user_service.create(
            schema=UserIn(name=fake.name(), email=fake.email(), oauth="test")
        )
        user = await user_service.delete_by_id(id=user.id)
    with pytest.raises(EntityNotFound):
        user = await user_service.delete_by_id(id=99999)
