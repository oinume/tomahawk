import logging

def create_logger(debug_enabled=False, deep_debug_enabled=False):
    level = logging.INFO
    if debug_enabled:
        level = logging.DEBUG
    if deep_debug_enabled:
        format = "[%(levelname)s] %(filename)s:%(lineno)d %(message)s"
    else:
        format = "[%(levelname)s] %(message)s"
    logging.basicConfig(
        level = level,
        format = format
    )
    return logging
