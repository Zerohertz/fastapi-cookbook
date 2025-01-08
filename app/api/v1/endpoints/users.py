from datetime import datetime
from sys import exception

from fastapi import APIRouter
from loguru import logger

from app.exceptions.users import (
    InsufficientFunds,
    InvalidInput,
    UnauthorizedAccess,
    UserNotFound,
)
from app.schemas.responses import ApiResponse
from app.schemas.users import User

router = APIRouter(prefix="/user", tags=["user"])


@router.get("", response_model=ApiResponse[User])
async def get_user(id: int):
    logger.info("[GET] User")
    try:
        if id == 1:
            raise InsufficientFunds
        if id == 2:
            raise InvalidInput
        if id == 3:
            raise UnauthorizedAccess("Unauthorized.")
        if id == 4:
            raise UserNotFound("User not found.")
        if id == 5:
            asdf
        if id == 6:
            10 / 0
        if id == 7:
            assert 1 == 0
    except Exception as error:
        logger.exception(repr(error))
        raise error
    return ApiResponse[User].success(
        status=200,
        data=User(id=id, created_at=datetime.now(), updated_at=datetime.now()),
    )
