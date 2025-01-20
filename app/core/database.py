from contextlib import contextmanager
from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from app.core.configs import configs
from app.models.base import BaseModel


class Database:
    def __init__(self) -> None:
        self.engine = create_engine(configs.DATABASE_URI, echo=configs.DB_ECHO)
        self.scoped_session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
            ),
        )

    def create_all(self) -> None:
        BaseModel.metadata.create_all(self.engine)

    @contextmanager
    def session(self) -> Generator[Any, Any, None]:
        session: Session = self.scoped_session()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
