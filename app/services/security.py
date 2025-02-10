from passlib.context import CryptContext


class CryptService(CryptContext):
    def __init__(self) -> None:
        super().__init__(schemes=["bcrypt"], deprecated="auto")

    def hash(self, secret: str) -> str:  # type: ignore[override]
        return super().hash(secret=secret)

    def verify(self, secret: str, hash: str) -> bool:  # type: ignore[override]
        return super().verify(secret=secret, hash=hash)
