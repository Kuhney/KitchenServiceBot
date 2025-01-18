"""Module containing the function to set up the logging configuration."""

import json
import logging.config
from pathlib import Path


def setup_logging() -> None:
    """Load the logging configuration from the logging.json file and set it globally."""
    with Path("logging.json").open() as file:
        logging_config = json.load(file)
        logging.config.dictConfig(logging_config)
