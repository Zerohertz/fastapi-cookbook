import logging

from loguru import logger


def remove_handler(_logger):
    for handler in _logger.handlers[:]:
        _logger.removeHandler(handler)


class LoguruHandler(logging.Handler):
    def emit(self, record):
        getattr(logger, record.levelname.lower(), logger.info)(record.getMessage())
