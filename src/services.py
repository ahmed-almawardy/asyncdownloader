"""Services to provide additional helpers to the main app."""

import base64
import hashlib
from datetime import datetime

from src.logger import logger


def log_started() -> None:
    """
    Write Logger head.

    :return:
    """
    logger.info('Starting app...')


def log_ended(started_at: datetime) -> None:
    """
    Write Logger tail.

    :param started_at:  datetime.datetime
    :return:
    """
    logger.info('Done.')
    timing = datetime.now() - started_at
    message = 'timing. ({0}) secs/ms'.format(timing.total_seconds())
    logger.info(message)
    line_length = 100
    logger.info('=' * line_length)


def hash_content(file_content: bytes) -> str:
    """
    Use for generating sha256 hash for raw buffered data.

    :param file_content: bytes data
    :return: str sha256 hash
    """
    encoded_b64 = base64.b64encode(file_content)
    return hashlib.sha256(encoded_b64).hexdigest()
