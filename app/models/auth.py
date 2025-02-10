from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.enums import OAuthProvider


class OAuth(BaseModel):
    __tablename__ = "oauth"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    provider: Mapped[OAuthProvider] = mapped_column(Enum(OAuthProvider), nullable=False)
    password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    oauth_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    oauth_token: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user = relationship("User", back_populates="oauth", lazy="noload")

    eagers = ["user"]

    __table_args__ = (
        UniqueConstraint("user_id", "provider", name="uq_oauth_user_provider"),
    )
