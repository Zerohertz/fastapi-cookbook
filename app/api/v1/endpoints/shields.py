from datetime import datetime

from fastapi.responses import ORJSONResponse

from app.core.router import CoreAPIRouter
from app.schemas.shields import Shields
from app.utils.shields import dday

router = CoreAPIRouter(prefix="/shields", tags=["shields.io"])


@router.get(
    "/jmy",
    response_model=Shields,
    response_class=ORJSONResponse,
    status_code=200,
    summary="",
    description="",
)
async def get_jmy():
    return Shields(
        schemaVersion=1,
        label="전문연구요원",
        message=f"D-{dday(datetime(2026, 2, 28))}",
        color="800a0a",
        labelColor="000",
        namedLogo="googlescholar",
        style="for-the-badge",
    )
