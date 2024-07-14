"""Main settings for logger."""

from logging import INFO, FileHandler, Formatter, StreamHandler, getLogger

logger = getLogger('INFO')
logger.setLevel(INFO)
formatter = Formatter('%(name)s: %(message)s  [%(asctime)s]')
stream_handler = StreamHandler()
file_handler = FileHandler('../app.log', mode='a+')
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
