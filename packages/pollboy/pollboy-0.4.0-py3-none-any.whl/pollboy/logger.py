from pollboy import settings
import os
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

def get_logger(name, file_path=None):

    log_path = file_path or settings.LOG_FILE

    # create logger
    logger = logging.getLogger(name)

    # This makes sure we don't keep adding additional handlers after they've been added the first time
    if(logger.hasHandlers()):
        return logger

    logger.setLevel(logging.DEBUG)

    # create console and file handlers and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.CONSOLE_LOG_LEVEL)
    file_handler = RotatingFileHandler(log_path, maxBytes=settings.FILE_LOG_MAX_BYTES, backupCount=settings.FILE_LOG_BACKUP_COUNT)
    file_handler.setLevel(settings.CONSOLE_LOG_LEVEL)

    # create formatter
    formatter = logging.Formatter(settings.LOG_FORMAT)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # add to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger