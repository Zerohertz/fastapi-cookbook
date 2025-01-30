from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase): ...


class BaseModel(Base):
    __abstract__ = True

    id = mapped_column(Integer, primary_key=True, nullable=False)
    created_at = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
