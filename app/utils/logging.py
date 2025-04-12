"""
This module sets up logging for the application.
It configures a logger to output logs to the console with a specific format.
"""

import logging
import sys

logger = logging.getLogger()
logging_format = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging_format)

logger.handlers = [stream_handler]
logger.setLevel(logging.INFO)
