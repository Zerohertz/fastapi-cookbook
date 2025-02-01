import time
from typing import Optional

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.core.database import database
from app.utils.logging import (
    ANSI_BG_COLOR,
    ANSI_FG_COLOR,
    ANSI_STYLE,
    ansi_format,
    osc_format,
)


class LoggingMiddleware(BaseHTTPMiddleware):
    def info(
        self,
        *,
        ip: str,
        url: str,
        method: str,
        status: Optional[str] = None,
        elapsed_time: Optional[str] = None,
    ) -> None:
        ip = osc_format(ip, href=f"https://db-ip.com/{ip}")
        ip = ansi_format(
            ip,
            bg_color=ANSI_BG_COLOR.LIGHT_BLACK,
            style=[ANSI_STYLE.UNDERLINE, ANSI_STYLE.BOLD],
        )
        ip = f"[IP: {ip}]"
        url = ansi_format(f"[URL: {url}]", fg_color=ANSI_FG_COLOR.LIGHT_BLACK)
        method = ansi_format(f"[Method: {method}]", fg_color=ANSI_FG_COLOR.LIGHT_BLACK)
        if status and elapsed_time:
            status = ansi_format(
                status,
                bg_color=ANSI_BG_COLOR.LIGHT_BLACK,
                style=[ANSI_STYLE.UNDERLINE, ANSI_STYLE.BOLD],
            )
            elapsed_time = ansi_format(
                elapsed_time,
                bg_color=ANSI_BG_COLOR.LIGHT_BLACK,
                style=[ANSI_STYLE.UNDERLINE, ANSI_STYLE.BOLD],
            )
            status = f"[Status: {status} (Elapsed Time: {elapsed_time})]"
        else:
            status = ansi_format(
                "[Status: Processing...]", fg_color=ANSI_FG_COLOR.LIGHT_BLACK
            )
        logger.info(f"{ip} {url} {method} {status}")

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.headers.get("x-real-ip"):
            ip = request.headers.get("x-real-ip")
        elif request.headers.get("x-forwarded-for"):
            ip = request.headers.get("x-forwarded-for")
        elif request.client:
            ip = request.client.host
        else:
            ip = "None"
        self.info(ip=str(ip), url=str(request.url), method=str(request.method))
        body = await request.body()
        if body:
            logger.trace(f"{body=}")
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        self.info(
            ip=str(ip),
            url=str(request.url),
            method=str(request.method),
            status=str(response.status_code),
            elapsed_time=f"{end_time - start_time:.3f}s",
        )
        return response


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            context = database.context.set(session_id=hash(request))
            logger.trace(f"[Session Start]\tID: {database.context.get()}, {context=}")
            response = await call_next(request)
        finally:
            await database.scoped_session.remove()
            logger.trace(f"[Session End]\tID: {database.context.get()}, {context=}")
            database.context.reset(context=context)
        return response
