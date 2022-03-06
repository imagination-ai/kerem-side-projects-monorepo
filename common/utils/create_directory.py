import os
import logging
from common.customized_logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


def create_directory(dir_path):
    try:
        os.mkdir(dir_path)
        logger.info(f"{dir_path} is created")
    except OSError:
        logger.info(f"Skipping creating {dir_path} since it exists.")
