"""Module for logging methods."""

from os import path
from sys import stdout
from logging import (getLogger, DEBUG, INFO, ERROR, Filter,
                     StreamHandler, FileHandler, Logger)


class ExcludeErrorFilter(Filter):
    """Filter object for exlcuding error logs."""

    def filter(self, record):
        """Return true when log level is not error."""
        return record.levelno != ERROR


def get_logger(enabled: bool) -> Logger:
    """Return logger with or without handlers."""
    ab = path.dirname(__file__)
    logger = getLogger("etl_logger")
    logger.setLevel(DEBUG)
    logger.propagate = False

    if logger.handlers:
        logger.handlers.clear()

    file_handler = FileHandler(f'{ab}/etl.log')
    file_handler.setLevel(ERROR)

    console_handler = StreamHandler(stdout)
    console_handler.setLevel(INFO)

    if enabled:
        logger.addHandler(file_handler)
        console_handler.addFilter(ExcludeErrorFilter())

    logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    logger = get_logger(False)
    logger.info("Logger Initiated.")
