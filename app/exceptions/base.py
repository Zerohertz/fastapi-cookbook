import abc


class BusinessException(abc.ABC, Exception):
    status: int
    message: str
