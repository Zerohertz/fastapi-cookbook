from sqlalchemy import Enum, String
from sqlalchemy.orm import mapped_column

from app.models.base import BaseModel
from app.models.enums import OAuthProvider, Role


class User(BaseModel):
    __tablename__ = "user"

    name = mapped_column(String(255), unique=True, nullable=False)
    # TODO: Email 검증
    email = mapped_column(String(255), unique=True, nullable=False)
    role = mapped_column(Enum(Role), unique=False, nullable=False)
    oauth = mapped_column(Enum(OAuthProvider), unique=False, nullable=False)
    password = mapped_column(String(255), unique=False, nullable=True)
    refresh_token = mapped_column(String(255), unique=False, nullable=True)
    oauth_token = mapped_column(String(255), unique=False, nullable=True)
