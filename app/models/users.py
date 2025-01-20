from sqlalchemy import Column, String

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    name = Column(String(255), unique=True)
