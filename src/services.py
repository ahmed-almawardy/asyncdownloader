"""
 Services to provide additional helpers to the main app
"""
import base64
import hashlib
import logging
from datetime import datetime
from logging import getLogger
from settings import DATE_FORMATE

logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.FileHandler('../app.log', mode='a+', ))


def log_started(started_at):
    """
    Logger head
    :param started_at:  datetime.datetime
    :return:
    """
    logger.info(f"{logger.name}: Starting app... at {started_at:{DATE_FORMATE}}")


def log_ended(started_at):
    """
    Logger tail
    :param started_at:  datetime.datetime
    :return:
    """
    logger.info(f"{logger.name}: Done. at {datetime.now():{DATE_FORMATE}}")
    timing = datetime.now() - started_at
    logger.info(f"{logger.name}: timing. {timing.total_seconds()} secs/mcs")
    logger.info('=' * 120)


def hash_content(content: bytes) -> str:
    """
    used for generating sha256 hash for raw buffered data.
    :param content: bytes data
    :return: str sha256 hash
    """
    encoded_b64 = base64.b64encode(content)
    return hashlib.sha256(encoded_b64).hexdigest()
