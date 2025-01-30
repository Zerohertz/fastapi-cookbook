from fastapi import APIRouter

from app.api.v1.endpoints import auth, shields, users

routers = APIRouter(prefix="/v1", tags=["v1"])
_routers = [auth.router, users.router, shields.router]

for _router in _routers:
    routers.include_router(_router)
