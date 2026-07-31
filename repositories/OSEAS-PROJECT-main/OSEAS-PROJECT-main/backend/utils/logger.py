"""Application-wide logging setup.

Replaces the bare print() call that used to run at import time in app.py
("FULL AI ENGAGEMENT SYSTEM RUNNING") with proper, configurable logging.
"""
import logging
import os
from logging.handlers import RotatingFileHandler


_CONFIGURED = False


def configure_logging(log_file: str, level: int = logging.INFO) -> None:
    """Configure the root application logger once.

    Args:
        log_file: Absolute path to the log file to write to.
        level: Logging level (defaults to INFO).
    """
    global _CONFIGURED
    if _CONFIGURED:
        return

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    root_logger = logging.getLogger("engagement_app")
    root_logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced logger under the ``engagement_app`` root logger.

    Args:
        name: Typically ``__name__`` of the calling module.
    """
    return logging.getLogger(f"engagement_app.{name}")
