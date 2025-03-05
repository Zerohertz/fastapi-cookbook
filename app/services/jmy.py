from app.core.database import database
from app.models.jmy import JmyCompany, JmyTimeSeries
from app.repositories.jmy import JmyRepository
from app.schemas.jmy import JmyCompanyOut, JmyCompanyRequest
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
