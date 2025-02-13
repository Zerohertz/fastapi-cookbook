from contextvars import ContextVar, Token
from functools import wraps
from typing import Awaitable, Callable

from loguru import logger
from sqlalchemy import AsyncAdaptedQueuePool, StaticPool, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.core.configs import ENVIRONMENT, configs
from app.models.auth import OAuth
from app.models.base import BaseModel
from app.models.enums import OAuthProvider, Role
from app.models.users import User
from app.services.security import CryptService


class Context:
    def __init__(self) -> None:
        self.context: ContextVar[int | None] = ContextVar(
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
        if configs.DB_TYPE == "sqlite":
            self.engine = create_async_engine(
                url=configs.DATABASE_URI,
                echo=configs.DB_ECHO,
                echo_pool=configs.DB_ECHO,
                poolclass=StaticPool,
                pool_pre_ping=True,
                pool_recycle=3600,
            )
        else:
            self.engine = create_async_engine(
                url=configs.DATABASE_URI,
                echo=configs.DB_ECHO,
                echo_pool=configs.DB_ECHO,
                max_overflow=10,
                poolclass=AsyncAdaptedQueuePool,
                pool_pre_ping=True,
                pool_size=5,
                pool_recycle=3600,
                pool_timeout=30.0,
            )
        self.sessionmaker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
        self.scoped_session = async_scoped_session(
            session_factory=self.sessionmaker,
            scopefunc=self.context.get,
        )

    async def create_all(self) -> None:
        logger.warning("Create database")
        async with self.engine.begin() as conn:
            if configs.ENV == ENVIRONMENT.TEST:
                await conn.run_sync(BaseModel.metadata.drop_all)
            await conn.run_sync(BaseModel.metadata.create_all)
        async with self.sessionmaker() as session:
            stmt = select(User).where(User.role == Role.ADMIN)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                logger.warning(f"Admin user already exists: {user}")
                return
            crypt_service = CryptService()
            user = User(
                name=configs.ADMIN_NAME,
                email=configs.ADMIN_EMAIL,
                role=Role.ADMIN,
                refresh_token=None,
                oauth=[
                    OAuth(
                        provider=OAuthProvider.PASSWORD,
                        password=crypt_service.hash(configs.ADMIN_PASSWORD),
                    )
                ],
            )
            session.add(user)
            await session.commit()

    def transactional(self, func: Callable[..., Awaitable]) -> Callable[..., Awaitable]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                session = self.scoped_session()
                if session.in_transaction():
                    logger.trace(f"[Session in transaction]\tID: {self.context.get()}")
                    return await func(*args, **kwargs)
                async with session.begin():
                    response = await func(*args, **kwargs)
                return response
            except Exception as error:
                raise error

        return wrapper


database = Database()
