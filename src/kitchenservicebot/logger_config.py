import json
import logging.config
from pathlib import Path


def setup_logging():
    with Path("logging.json").open() as file:
        logging_config = json.load(file)
        logging.config.dictConfig(logging_config)
