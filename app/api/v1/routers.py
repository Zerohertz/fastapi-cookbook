from fastapi import APIRouter

from app.api.v1.endpoints import users

routers = APIRouter(prefix="/v1")
_routers = [users.router]

for _router in _routers:
    _router.tags = _router.tags.append("v1")
    routers.include_router(_router)