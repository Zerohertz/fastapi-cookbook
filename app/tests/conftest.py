from collections.abc import Generator
from contextvars import Token
from typing import AsyncGenerator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from loguru import logger

from app.core.container import Container
from app.core.database import database
from app.main import app

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
async def context() -> AsyncGenerator[Token, None]:
    _context = database.context.set(session_id=hash(uuid4()))
    logger.error(database.context.get())
    yield _context
    # NOTE: PyTest 시 event loop 충돌 발생 (related: #19)
    await database.engine.dispose()
    database.context.reset(context=_context)


@pytest.fixture(scope="session")
def container() -> Generator[Container, None, None]:
    _container = Container()
    _container.wire()
    yield _container


@pytest.fixture(scope="module")
def sync_client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
