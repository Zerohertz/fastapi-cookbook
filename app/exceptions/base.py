import abc


class CoreException(abc.ABC, Exception):
    status: int
    message: str
