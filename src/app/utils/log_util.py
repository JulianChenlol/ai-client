import logging
import os
import sys
from logging import handlers

LOG_LEVEL = os.environ.get("SERVICE_LOG_LEVEL", "DEBUG")

default_formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s",
)
stream_handler = logging.StreamHandler(stream=sys.stderr)
stream_handler.setLevel(LOG_LEVEL)
stream_handler.setFormatter(default_formatter)

# file_handler = logging.FileHandler("src/app/logs/service.log")
# file_handler.setLevel(LOG_LEVEL)
# file_handler.setFormatter(default_formatter)
time_rotating_file_handler = handlers.TimedRotatingFileHandler(
    filename="src/app/logs/daily.log", when="D"
)
time_rotating_file_handler.setLevel(LOG_LEVEL)
time_rotating_file_handler.setFormatter(default_formatter)

logger = logging.getLogger(__name__)
logger.addHandler(stream_handler)
logger.addHandler(time_rotating_file_handler)

logger.setLevel(LOG_LEVEL)
logger.propagate = False
