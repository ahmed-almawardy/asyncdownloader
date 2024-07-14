"""Services to provide additional helpers to the main app."""

import base64
import hashlib
from datetime import datetime
from logging import INFO, FileHandler, StreamHandler, getLogger, Formatter

logger = getLogger('LOG')
logger.setLevel(INFO)
formatter = Formatter('%(name)s: %(message)s  [%(asctime)s]')
stream_handler = StreamHandler()
file_handler = FileHandler('../app.log', mode='a+')
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def log_started(started_at):
    """
    Write Logger head.

    :param started_at:  datetime.datetime
    :return:
    """
    logger.info('Starting app...')


def log_ended(started_at):
    """
    Write Logger tail.

    :param started_at:  datetime.datetime
    :return:
    """
    logger.info('Done.')
    timing = datetime.now() - started_at
    logger.info('timing. (%s) secs/ms', timing.total_seconds())
    line_length = 120
    logger.info('=' * line_length)


def hash_content(file_content: bytes) -> str:
    """
    Use for generating sha256 hash for raw buffered data.

    :param file_content: bytes data
    :return: str sha256 hash
    """
    encoded_b64 = base64.b64encode(file_content)
    return hashlib.sha256(encoded_b64).hexdigest()
