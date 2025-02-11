from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.enums import Role


class User(BaseModel):
    __tablename__ = "user"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    # TODO: 우선은 email이 동일한 계정들은 동일 인물로 가정
    # 차후 인증이 완료된 사용자는 OAuth를 추가할 수 있도록
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    refresh_token: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # NOTE: one-to-many
    # WARN: Async DB session에서 명시적이지 않은 IO는 권장되지 않는다.
    # lazy="noload"는 삭제될거 같은... (related: #38)
    oauth = relationship(
        "OAuth", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )

    eagers = ["oauth"]
