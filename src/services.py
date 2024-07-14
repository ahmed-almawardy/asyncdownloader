"""Services to provide additional helpers to the main app."""

import base64
import hashlib
from datetime import datetime
from logging import INFO, FileHandler, StreamHandler, getLogger


logger = getLogger('APP')
logger.setLevel(INFO)
logger.addHandler(StreamHandler())
logger.addHandler(FileHandler('../app.log', mode='a+'))


def log_started(started_at):
    """
    Write Logger head.

    :param started_at:  datetime.datetime
    :return:
    """
    logger.info(f'{logger.name}: Starting app... {started_at}')


def log_ended(started_at):
    """
    Write Logger tail.

    :param started_at:  datetime.datetime
    :return:
    """
    logger.info(f'{logger.name}: Done. at {datetime.now()}')
    timing = datetime.now() - started_at
    logger.info(f'{logger.name}: timing. {timing.total_seconds()} secs/ms')
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
