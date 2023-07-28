import logging
import sys
from collections import namedtuple
from typing import Callable, Optional, Awaitable

from hypercorn.config import Config as HyperCornConfig
from loguru import logger

from duodrone.data import OuterEvent

LoggingConfig = namedtuple('LoggingFormat', ['format', 'level'])


class DuodroneLoggingConfig:
    use_default_loggers: bool = True
    format: str = ("<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | " \
                   "<level>{level: <5}</level> | " \
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | " \
                   "<level>{message}</level>")
    """source: https://github.com/Delgan/loguru/issues/586#issuecomment-1030819250"""
    level: str = "INFO"


class LoguruInterceptHandler(logging.Handler):
    """
    Intercept python logging module logs to loguru.
    https://stackoverflow.com/a/65331310/11397457
    https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record):
        # Get corresponding Loguru level if it exists.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = logging.currentframe(), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class DuodroneConfig:
    """
    Configurations for duodrone module.
    """

    __instance: 'DuodroneConfig' = None

    debug: bool = False

    logger: DuodroneLoggingConfig = DuodroneLoggingConfig()

    outer_event_handler: Callable[[OuterEvent], None] = lambda self, resp: print(f'Dummy get outer response: {resp}')
    """outer event handler"""

    hypercorn_config = HyperCornConfig()
    """hypercorn config"""

    hypercorn_shutdown_trigger: Optional[Callable[..., Awaitable[None]]] = None
    """hypercorn shutdown trigger"""

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DuodroneConfig, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        """Default configs"""

        # Armor Class 15 (natural armor), Hit Points 11 (2d8 + 2)
        self.hypercorn_config.bind = 'localhost:1511'

    def config_behaviors(self):
        self.config_logging()

    def config_logging(self):
        # remove default logging sink (stderr)
        logger.remove()

        # add loguru intercept handler to dependencies' loggers
        logging.basicConfig(handlers=[LoguruInterceptHandler()], level=0, force=True)

        if self.logger.use_default_loggers:
            logger_format = self.logger.format
            log_level = self.logger.level

            # https://clig.dev/#the-basics
            # access logs (logger.bind(a=True).info(...)) to stdout
            logger.add(sys.stdout, filter=lambda record: "a" in record["extra"], format=logger_format, level=log_level, enqueue=True)
            # other logs to stderr
            logger.add(sys.stderr, filter=lambda record: "a" not in record["extra"], format=logger_format, level=log_level, enqueue=True)
