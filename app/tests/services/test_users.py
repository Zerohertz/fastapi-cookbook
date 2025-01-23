from contextvars import Token

import pytest
from loguru import logger

from app.core.container import Container
from app.schemas.users import UserCreateRequest


@pytest.mark.asyncio(loop_scope="function")
async def test_create_user(container: Container, context: Token) -> None:
    logger.warning(f"{context=}")
    name = "service-layer-user"
    user_service = container.user_service()
    user = await user_service.create(schema=UserCreateRequest(name=name))
    assert user.name == name
