from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class JmyCompany(BaseModel):
    __tablename__ = "jmy_company"

    # 업체명
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # 선정년도
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    # 지방청
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    # 주소
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    # 업종
    type_: Mapped[str] = mapped_column("type", String(255), nullable=False)
    # 기업규모
    size: Mapped[str] = mapped_column(String(255), nullable=False)
    # 연구분야
    research: Mapped[str] = mapped_column(String(255), nullable=True)

    time_series = relationship(
        "JmyTimeSeries",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    eagers = ["time_series"]


class JmyTimeSeries(BaseModel):
    __tablename__ = "jmy_time_series"

    company_id: Mapped[int] = mapped_column(
        ForeignKey("jmy_company.id"), nullable=False
    )

    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    # 보충역 배정인원
    b_assigned: Mapped[int] = mapped_column(Integer, nullable=False)
    # 보충역 편입인원
    b_new: Mapped[int] = mapped_column(Integer, nullable=False)
    # 보충역 복무인원
    b_old: Mapped[int] = mapped_column(Integer, nullable=False)
    # 현역 배정인원
    a_assigned: Mapped[int] = mapped_column(Integer, nullable=False)
    # 현역 편입인원
    a_new: Mapped[int] = mapped_column(Integer, nullable=False)
    # 현역 복무인원
    a_old: Mapped[int] = mapped_column(Integer, nullable=False)

    company = relationship("JmyCompany", back_populates="time_series", lazy="noload")

    eagers = ["company"]
