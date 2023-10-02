from __future__ import annotations

import logging
import sys

from typing_extensions import override

__all__ = ["logger"]

GREY = "\x1b[38;20m"
YELLOW = "\x1b[33;20m"
RED = "\x1b[31;20m"
BOLD_RED = "\x1b[31;1m"
RESET = "\x1b[0m"

LOG_FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
)
LOG_COLORS = {
    logging.DEBUG: GREY + LOG_FORMAT + RESET,
    logging.INFO: GREY + LOG_FORMAT + RESET,
    logging.WARNING: YELLOW + LOG_FORMAT + RESET,
    logging.ERROR: RED + LOG_FORMAT + RESET,
    logging.CRITICAL: BOLD_RED + LOG_FORMAT + RESET,
}


class ColorFormatter(logging.Formatter):
    @override
    def format(self, record: logging.LogRecord) -> str:
        log_fmt = LOG_COLORS.get(record.levelno, LOG_FORMAT)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("diskcache.fernet")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(ColorFormatter())
logger.addHandler(handler)
