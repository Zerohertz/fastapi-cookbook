from collections.abc import Generator
from contextvars import Token
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from app.core.container import Container
from app.core.database import database
from app.main import app


@pytest_asyncio.fixture(scope="function")
async def context() -> AsyncGenerator[Token, None]:
    _context = database.context.set(session_id=hash(123))
    yield _context
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


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
