import logging
from enum import Enum
from typing import Optional

from loguru import logger


def remove_handler(_logger: logging.Logger) -> None:
    for handler in _logger.handlers[:]:
        _logger.removeHandler(handler)


def update_logger_format():
    for logger_name, _logger in logging.Logger.manager.loggerDict.items():
        if isinstance(_logger, logging.Logger):
            if not _logger.handlers:
                continue
            for handler in _logger.handlers:
                handler.setFormatter(
                    logging.Formatter(
                        "%(asctime)s | %(levelname)s | %(name)s - %(message)s"
                    )
                )


class LoguruHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        getattr(logger, record.levelname.lower(), logger.info)(record.getMessage())


class ANSI_STYLE(Enum):
    BOLD = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    INVERSE = 7
    HIDDEN = 8


class ANSI_FG_COLOR(Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    LIGHT_BLACK = 90
    LIGHT_RED = 91
    LIGHT_GREEN = 92
    LIGHT_YELLOW = 93
    LIGHT_BLUE = 94
    LIGHT_MAGENTA = 95
    LIGHT_CYAN = 96
    LIGHT_WHITE = 97


class ANSI_BG_COLOR(Enum):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    LIGHT_BLACK = 100
    LIGHT_RED = 101
    LIGHT_GREEN = 102
    LIGHT_YELLOW = 103
    LIGHT_BLUE = 104
    LIGHT_MAGENTA = 105
    LIGHT_CYAN = 106
    LIGHT_WHITE = 107


def ansi_format(
    text: str | int,
    *,
    fg_color: Optional[ANSI_FG_COLOR] = None,
    bg_color: Optional[ANSI_BG_COLOR] = None,
    style: Optional[ANSI_STYLE | list[ANSI_STYLE]] = None,
) -> str:
    args = []
    if fg_color:
        args.append(str(fg_color.value))
    if bg_color:
        args.append(str(bg_color.value))
    if style:
        if not isinstance(style, list):
            style = [style]
        for _style in style:
            args.append(str(_style.value))
    return f"""\033[{";".join(args)}m{text}\033[0m"""


def osc_format(text: str, *, href: str) -> str:
    return f"\033]8;;{href}\033\\{text}\033]8;;\033\\"
