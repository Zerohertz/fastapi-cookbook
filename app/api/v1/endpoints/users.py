from datetime import datetime

from loguru import logger

from app.core.router import CoreAPIRouter
from app.exceptions.users import (
    InsufficientFunds,
    InvalidInput,
    UnauthorizedAccess,
    UserNotFound,
)
from app.schemas.users import User

router = CoreAPIRouter(prefix="/user", tags=["user"])


@router.get(
    "",
    response_model=User,
    status_code=200,
    summary="Get User Test",
    description="1 ~ 4: Error!",
)
async def get_user(user_id: int):
    logger.info("[GET] User")
    try:
        if user_id == 1:
            raise InsufficientFunds
        if user_id == 2:
            raise InvalidInput
        if user_id == 3:
            raise UnauthorizedAccess("Unauthorized.")
        if user_id == 4:
            raise UserNotFound("User not found.")
    except Exception as error:
        logger.exception(repr(error))
        raise error
    return User(id=user_id, created_at=datetime.now(), updated_at=datetime.now())
