from contextlib import asynccontextmanager
from typing import Any, Generator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from app.core.configs import configs
from app.models.base import BaseModel


class Database:
    def __init__(self) -> None:
        self.engine = create_async_engine(configs.DATABASE_URI, echo=configs.DB_ECHO)
        self.sessionmaker = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_all(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> Generator[Any, Any, None]:
        async with self.sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
