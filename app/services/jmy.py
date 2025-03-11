from typing import Literal

from app.core.database import database
from app.models.jmy import JmyCompany, JmyTimeSeries
from app.repositories.jmy import JmyRepository
from app.schemas.jmy import (
    JmyCompanyInfo,
    JmyCompanyOut,
    JmyCompanyRequest,
    JmyPageResponse,
)
from app.services.base import BaseService


class JmyService(BaseService[JmyCompany, JmyCompanyRequest, JmyCompanyOut]):
    def __init__(self, jmy_repository: JmyRepository):
        super().__init__(repository=jmy_repository, schema=JmyCompanyOut)
        self.repository: JmyRepository

    @database.transactional
    async def create(self, schema: JmyCompanyRequest) -> JmyCompanyOut:
        jmy_company = await self.repository.read_by_name(name=schema.name)
        if jmy_company is None:
            jmy_company = JmyCompany(
                name=schema.name,
                year=schema.year,
                location=schema.location,
                address=schema.address,
                type_=schema.type_,
                size=schema.size,
                research=schema.research,
            )
        jmy_company.time_series.append(
            JmyTimeSeries(
                date=schema.date,
                b_assigned=schema.b_assigned,
                b_new=schema.b_new,
                b_old=schema.b_old,
                a_assigned=schema.a_assigned,
                a_new=schema.a_new,
                a_old=schema.a_old,
            )
        )
        entity = await self.repository.create(entity=jmy_company)
        return self.mapper(entity)

    @database.transactional
    async def get_page(
        self,
        page: int,
        size: int,
        sort_by: Literal["old", "new"],
        filter_by: Literal["ms", "phd", "all"],
    ) -> JmyPageResponse:
        entities, total_pages = await self.repository.read_page(
            page=page, size=size, sort_by=sort_by, filter_by=filter_by
        )
        jmy_company_info = []
        for entity in entities:
            time_series = entity.time_series[-1]
            jmy_company_info.append(
                JmyCompanyInfo(
                    id=entity.id,
                    created_at=entity.created_at,
                    updated_at=entity.updated_at,
                    name=entity.name,
                    year=entity.year,
                    location=entity.location,
                    address=entity.address,
                    type_=entity.type_,
                    size=entity.size,
                    research=entity.research,
                    date=time_series.date,
                    b_assigned=time_series.b_assigned,
                    b_new=time_series.b_new,
                    b_old=time_series.b_old,
                    a_assigned=time_series.a_assigned,
                    a_new=time_series.a_new,
                    a_old=time_series.a_old,
                )
            )
        return JmyPageResponse(info=jmy_company_info, total_pages=total_pages)
