from datetime import datetime

from app.schemas.base import BaseDBResponse, BaseRequest, BaseResponse


class JmyCompanyRequest(BaseRequest):
    name: str
    year: int
    location: str
    address: str
    type_: str
    size: str
    research: str
    date: datetime
    b_assigned: int
    b_new: int
    b_old: int
    a_assigned: int
    a_new: int
    a_old: int


class JmyCompanyResponse(BaseDBResponse):
    name: str
    year: int
    location: str
    address: str
    type_: str
    size: str
    research: str


class JmyCompanyInfo(JmyCompanyResponse):
    date: datetime
    b_assigned: int
    b_new: int
    b_old: int
    a_assigned: int
    a_new: int
    a_old: int


class JmyPageResponse(BaseResponse):
    info: list[JmyCompanyInfo]
    total_pages: int


class JmyTimeSeriesOut(BaseDBResponse):
    date: datetime
    b_assigned: int
    b_new: int
    b_old: int
    a_assigned: int
    a_new: int
    a_old: int


class JmyCompanyOut(JmyCompanyResponse):
    time_series: list[JmyTimeSeriesOut]
