import logging
import os
import sys

import json_logging
from fastapi import FastAPI

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


def get_logger(app: FastAPI, name: str) -> logging.Logger:
    app.get
    logger = logging.getLogger(name)
    logger.setLevel(logging.getLevelName(LOG_LEVEL))
    logger.addHandler(logging.StreamHandler(sys.stdout))
    json_logging.init_fastapi(enable_json=True)
    if LOG_LEVEL == "debug":
        json_logging.init_request_instrument(app)
    return logger
