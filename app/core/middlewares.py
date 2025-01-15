import time

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.utils.logging import ANSI_BG_COLOR, ANSI_STYLE, ansi_format


class LoggingMiddleware(BaseHTTPMiddleware):
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
        ip = ansi_format(
            f"{ip}",
            bg_color=ANSI_BG_COLOR.LIGHT_BLACK,
            style=[ANSI_STYLE.UNDERLINE, ANSI_STYLE.BOLD],
        )
        url = ansi_format(
            str(request.url),
            bg_color=ANSI_BG_COLOR.LIGHT_BLACK,
            style=[ANSI_STYLE.UNDERLINE],
        )
        method = ansi_format(
            request.method,
            bg_color=ANSI_BG_COLOR.LIGHT_BLACK,
            style=[ANSI_STYLE.UNDERLINE],
        )
        status = ansi_format(
            "Processing...",
            bg_color=ANSI_BG_COLOR.LIGHT_BLACK,
            style=[ANSI_STYLE.UNDERLINE],
        )
        logger.info(f"[IP: {ip}] [URL: {url}] [Method: {method}] [Status: {status}]")
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        status = ansi_format(
            str(response.status_code),
            bg_color=ANSI_BG_COLOR.LIGHT_BLACK,
            style=[ANSI_STYLE.UNDERLINE, ANSI_STYLE.BOLD],
        )
        elapsed_time = ansi_format(
            f"{end_time - start_time:.3f}s",
            bg_color=ANSI_BG_COLOR.LIGHT_BLACK,
            style=[ANSI_STYLE.UNDERLINE, ANSI_STYLE.BOLD],
        )
        logger.info(
            f"[IP: {ip}] [URL: {url}] [Method: {method}] [Status: {status} (Elapsed Time: {elapsed_time})]"
        )
        return response
