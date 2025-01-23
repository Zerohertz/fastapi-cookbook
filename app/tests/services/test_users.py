from contextvars import Token

import pytest
from loguru import logger
from sqlalchemy import schema

from app.core.container import Container
from app.exceptions.database import EntityAlreadyExists, EntityNotFound
from app.schemas.users import UserCreateRequest


@pytest.mark.asyncio(loop_scope="function")
async def test_create_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    name = "service-layer-user"
    user_service = container.user_service()
    for id in range(10):
        _name = f"{name}-{id}"
        user = await user_service.create(schema=UserCreateRequest(name=_name))
        assert user.name == _name
    with pytest.raises(EntityAlreadyExists):
        user = await user_service.create(schema=UserCreateRequest(name=_name))


@pytest.mark.asyncio(loop_scope="function")
async def test_get_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    name = "service-layer-user"
    user_service = container.user_service()
    for id in range(10, 20):
        _name = f"{name}-{id}"
        user = await user_service.create(schema=UserCreateRequest(name=_name))
        user = await user_service.get_by_id(id=user.id)
        assert user.name == _name
    with pytest.raises(EntityNotFound):
        user = await user_service.get_by_id(id=99999)


@pytest.mark.asyncio(loop_scope="function")
async def test_put_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    name = "service-layer-user"
    user_service = container.user_service()
    for id in range(20, 30):
        _name = f"{name}-{id}"
        user = await user_service.create(schema=UserCreateRequest(name=_name))
        _name = f"{name}-put-{id}"
        user = await user_service.put_by_id(
            id=user.id, schema=UserCreateRequest(name=_name)
        )
        assert user.name == _name
    with pytest.raises(EntityNotFound):
        user = await user_service.put_by_id(
            id=99999, schema=UserCreateRequest(name=name)
        )


@pytest.mark.asyncio(loop_scope="function")
async def test_patch_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    name = "service-layer-user"
    user_service = container.user_service()
    for id in range(30, 40):
        _name = f"{name}-{id}"
        user = await user_service.create(schema=UserCreateRequest(name=_name))
        _name = f"{name}-patch-{id}"
        user = await user_service.patch_by_id(
            id=user.id, schema=UserCreateRequest(name=_name)
        )
        assert user.name == _name
        _name = f"{name}-patch-{id}-2"
        user = await user_service.patch_attr_by_id(id=user.id, attr="name", value=_name)
        assert user.name == _name
    with pytest.raises(EntityNotFound):
        user = await user_service.patch_by_id(
            id=99999, schema=UserCreateRequest(name=name)
        )
    with pytest.raises(EntityNotFound):
        user = await user_service.patch_attr_by_id(id=99999, attr="name", value=name)


@pytest.mark.asyncio(loop_scope="function")
async def test_delete_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    name = "service-layer-user"
    user_service = container.user_service()
    for _ in range(0, 10):
        user = await user_service.create(schema=UserCreateRequest(name=name))
        user = await user_service.delete_by_id(id=user.id)
    with pytest.raises(EntityNotFound):
        user = await user_service.delete_by_id(id=99999)
