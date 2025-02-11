import time

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
        status: int | None = None,
        elapsed_time: str | None = None,
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
            if status < 400:
                _status = ansi_format(
                    status,
                    bg_color=ANSI_BG_COLOR.LIGHT_BLACK,
                    style=[ANSI_STYLE.UNDERLINE, ANSI_STYLE.BOLD],
                )
            elif status < 500:
                _status = ansi_format(
                    status,
                    fg_color=ANSI_FG_COLOR.BLACK,
                    bg_color=ANSI_BG_COLOR.LIGHT_YELLOW,
                    style=[ANSI_STYLE.UNDERLINE, ANSI_STYLE.BOLD],
                )
            else:
                _status = ansi_format(
                    status,
                    bg_color=ANSI_BG_COLOR.RED,
                    style=[ANSI_STYLE.UNDERLINE, ANSI_STYLE.BOLD],
                )
            elapsed_time = ansi_format(
                elapsed_time,
                bg_color=ANSI_BG_COLOR.LIGHT_BLACK,
                style=[ANSI_STYLE.UNDERLINE, ANSI_STYLE.BOLD],
            )
            _status = f"[Status: {_status} (Elapsed Time: {elapsed_time})]"
        else:
            _status = ansi_format(
                "[Status: Processing...]", fg_color=ANSI_FG_COLOR.LIGHT_BLACK
            )
        logger.info(f"{ip} {url} {method} {_status}")

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
        self.info(ip=str(ip), url=str(request.url), method=request.method)
        body = await request.body()
        if body:
            logger.trace(f"{body=}")
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        self.info(
            ip=str(ip),
            url=str(request.url),
            method=request.method,
            status=response.status_code,
            elapsed_time=f"{end_time - start_time:.3f}s",
        )
        return response


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        context = database.context.set(session_id=hash(request))
        logger.trace(f"[Session Start]\tID: {database.context.get()}")
        try:
            response = await call_next(request)
        finally:
            await database.scoped_session.remove()
            logger.trace(f"[Session End]\tID: {database.context.get()}")
            database.context.reset(context=context)
        return response
