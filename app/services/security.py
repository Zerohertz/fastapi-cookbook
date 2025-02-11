from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from app.exceptions.auth import PasswordOAuthFailed


class CryptService(CryptContext):
    def __init__(self) -> None:
        super().__init__(schemes=["bcrypt"], deprecated="auto")

    def hash(self, secret: str) -> str:  # type: ignore[override]
        return super().hash(secret=secret)

    def verify(self, secret: str, hash: str) -> bool:  # type: ignore[override]
        try:
            return super().verify(secret=secret, hash=hash)
        except UnknownHashError as error:
            # TODO: 언제 UnknownHashError가 발생하는지 확인
            raise PasswordOAuthFailed from error
