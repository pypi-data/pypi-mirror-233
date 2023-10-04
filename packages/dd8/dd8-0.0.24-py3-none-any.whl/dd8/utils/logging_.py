# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 21:00:00 2023

@author: yqlim
"""
import logging
import logging.handlers

def get_default_formatter() -> logging.Formatter:
    return logging.Formatter(
        '%(asctime)s | %(name)s |  %(levelname)s: %(message)s'
    )

def get_default_stream_handler(
    logging_level: int=logging.INFO) -> logging.StreamHandler:

    formatter = get_default_formatter()
    handler = logging.StreamHandler()
    handler.setLevel(logging_level)
    handler.setFormatter(formatter)
    return handler

def get_default_file_handler(filepath: str,
    logging_level: int=logging.INFO) -> logging.handlers.TimedRotatingFileHandler:

    formatter = get_default_formatter()
    handler = logging.handlers.TimedRotatingFileHandler(
        filename=filepath, when='midnight', backupCount=30
    )
    handler.setLevel(logging_level)
    handler.setFormatter(formatter)
    return handler
