import logging
from typing import List

_levels = {
    "critical": logging.CRITICAL,
    "debug": logging.DEBUG,
    "error": logging.ERROR,
    "fatal": logging.FATAL,
    "info": logging.INFO,
    "warning": logging.WARNING,
}

LOGGER = {"main": logging.getLogger("main"),
          "popup": logging.getLogger("popup")}


def log(message:str, loggers: List[str], level: str):
    """Logs a message of a given level on the defined loggers.

    Args:
        message: the message to log
        loggers: the loggers on which the message should be logged
        level: the level of the message
    """
    for logger in loggers:
        LOGGER[logger].log(_levels[level], message)
