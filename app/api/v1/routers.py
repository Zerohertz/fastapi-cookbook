from fastapi import APIRouter

from app.api.v1.endpoints import auth, shields, users
from app.api.v1.endpoints.admin import jmy as admin_jmy
from app.api.v1.endpoints.admin import users as admin_users

routers = APIRouter(prefix="/v1", tags=["v1"])
_routers = [auth.router, users.router, shields.router] + [
    admin_users.router,
    admin_jmy.router,
]

for _router in _routers:
    routers.include_router(_router)
