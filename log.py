#!/usr/bin/env python
# -*- encoding=utf8 -*-
import logging
import logging.handlers

LOG_FILENAME = 'Relationship-Maintenance.log'

logger = logging.getLogger()


def set_logger():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(funcName)s %(lineno)s %(levelname)s - %(message)s",
                                  "%Y-%m-%d %H:%M:%S")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=10485760, backupCount=5, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


set_logger()
