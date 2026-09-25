"""
utils/logger.py
----------------
Single place to configure logging for the whole app: writes to logs/import.log
and echoes to the console.
"""

import logging
import os

import config


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # already configured (avoid duplicate handlers)

    logger.setLevel(logging.INFO)

    os.makedirs(os.path.dirname(config.LOG_FILE_PATH), exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(config.LOG_FILE_PATH, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
