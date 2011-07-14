import logging

def create_logger(debug_enabled=False):
    level = logging.INFO
    if debug_enabled:
        level = logging.DEBUG
    logging.basicConfig(
        level = level,
        format = '[%(levelname)s] %(message)s'
    )
    return logging
