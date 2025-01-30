from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    name = mapped_column(String(255), unique=True, nullable=False)
    email = mapped_column(String(255), unique=True, nullable=False)
    oauth = mapped_column(String(255), unique=False, nullable=False)
    password = mapped_column(String(255), unique=False, nullable=True)
    refresh_token = mapped_column(String(255), unique=False, nullable=True)
    github_token = mapped_column(String(255), unique=False, nullable=True)
