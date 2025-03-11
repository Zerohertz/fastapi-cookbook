import math
from operator import and_
from typing import Literal, Sequence

from sqlalchemy import func, select

from app.core.database import database
from app.models.jmy import JmyCompany, JmyTimeSeries
from app.repositories.base import BaseRepository


class JmyRepository(BaseRepository[JmyCompany]):
    def __init__(self):
        super().__init__(model=JmyCompany)

    async def read_by_name(self, name: str, eager: bool = False) -> JmyCompany | None:
        stmt = select(self.model)
        if eager:
            stmt = self._eager(stmt=stmt)
        stmt = stmt.where(self.model.name == name)
        session = database.scoped_session()
        result = await session.execute(stmt)
        entity = result.scalar_one_or_none()
        return entity

    async def read_page(
        self,
        page: int,
        size: int,
        sort_by: Literal["old", "new"],
        filter_by: Literal["ms", "phd", "all"],
    ) -> tuple[Sequence[JmyCompany], int]:
        jmy_ms = [
            "벤처기업부설연구소",
            "중견기업부설연구소",
            "중소기업부설연구소",
        ]
        latest_date_subq = (
            select(
                JmyTimeSeries.company_id, func.max(JmyTimeSeries.date).label("max_date")
            )
            .group_by(JmyTimeSeries.company_id)
            .subquery()
        )
        total_expr = (
            (JmyTimeSeries.b_old + JmyTimeSeries.a_old)
            if sort_by == "old"
            else (JmyTimeSeries.b_new + JmyTimeSeries.a_new)
        )
        total_subq = (
            select(
                JmyTimeSeries.company_id,
                total_expr.label("total"),
            )
            .join(
                latest_date_subq,
                and_(
                    JmyTimeSeries.company_id == latest_date_subq.c.company_id,
                    JmyTimeSeries.date == latest_date_subq.c.max_date,
                ),
            )
            .subquery()
        )
        stmt = select(self.model).outerjoin(
            total_subq, self.model.id == total_subq.c.company_id
        )
        if filter_by == "ms":
            stmt = stmt.where(self.model.type_.in_(jmy_ms))
        elif filter_by == "phd":
            stmt = stmt.where(self.model.type_.notin_(jmy_ms))
        offset = (page - 1) * size
        stmt = stmt.order_by(total_subq.c.total.desc()).offset(offset).limit(size)
        session = database.scoped_session()
        results = await session.execute(stmt)
        entities = results.scalars().all()
        _stmt = select(func.count(self.model.id)).outerjoin(
            total_subq, self.model.id == total_subq.c.company_id
        )
        if filter_by == "ms":
            _stmt = _stmt.where(self.model.type_.in_(jmy_ms))
        elif filter_by == "phd":
            _stmt = _stmt.where(self.model.type_.notin_(jmy_ms))
        result = await session.execute(_stmt)
        total_count = result.scalar_one()
        total_pages = math.ceil(total_count / size)
        return entities, total_pages
