from sqlalchemy import Enum, String, null
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel
from app.models.enums import OAuthProvider, Role


class User(BaseModel):
    __tablename__ = "user"

    name = mapped_column(String(255), unique=True, nullable=False)
    email = mapped_column(String(255), unique=True, nullable=False)
    role = mapped_column(Enum(Role), unique=False, nullable=False)
    oauth = mapped_column(Enum(OAuthProvider), unique=False, nullable=False)
    password = mapped_column(String(255), unique=False, nullable=True)
    refresh_token = mapped_column(String(255), unique=False, nullable=True)
    github_token = mapped_column(String(255), unique=False, nullable=True)
