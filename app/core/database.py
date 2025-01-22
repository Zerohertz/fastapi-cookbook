from contextvars import ContextVar, Token
from functools import wraps
from typing import Awaitable, Callable, Optional

from loguru import logger
from sqlalchemy import ClauseElement, Connection, Engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session as SyncSession
from sqlalchemy.orm.session import _EntityBindKey
from sqlalchemy.sql.expression import Delete, Insert, Update

from app.core.configs import configs
from app.models.base import BaseModel


class Context:
    def __init__(self) -> None:
        self.context: ContextVar[Optional[int]] = ContextVar(
            "session_context", default=None
        )

    def get(self) -> int:
        session_id = self.context.get()
        if not session_id:
            raise ValueError("Currently no session is available.")
        return session_id

    def set(self, session_id: int) -> Token:
        return self.context.set(session_id)

    def reset(self, context: Token) -> None:
        self.context.reset(context)


class Database:
    def __init__(self) -> None:
        self.context = Context()
        self.engine = create_async_engine(configs.DATABASE_URI, echo=configs.DB_ECHO)
        self.sessionmaker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
        self.scoped_session = async_scoped_session(
            session_factory=self.sessionmaker, scopefunc=self.context.get
        )

    async def create_all(self) -> None:
        logger.warning("Create database")
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

    def transactional(self, func: Callable[..., Awaitable]) -> Callable[..., Awaitable]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                session = self.scoped_session()
                if session.in_transaction():
                    logger.trace(
                        f"[Session in transaction]\tID: {database.context.get()}, {self.context=}"
                    )
                    return await func(*args, **kwargs)
                async with session.begin():
                    response = await func(*args, **kwargs)
                return response
            except Exception as error:
                raise error

        return wrapper


database = Database()
