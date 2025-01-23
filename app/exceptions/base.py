import abc


class CoreException(abc.ABC, Exception):
    status: int
    message: str

    def __str__(self) -> str:
        return (
            f"[{self.__class__.__name__}] status={self.status}, message={self.message}"
        )

    def __repr__(self) -> str:
        return f"[{self.__class__.__name__}] {self.message}"
