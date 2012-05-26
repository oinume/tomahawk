import logging
import sys

def create_logger(file_path = None, debug_enabled = False, deep_debug_enabled = False):
    level = logging.INFO
    if debug_enabled:
        level = logging.DEBUG
    if deep_debug_enabled:
        format = "[%(levelname)s] %(filename)s:%(lineno)d %(message)s"
    else:
        format = "[%(levelname)s] %(message)s"

    kwargs = { 'level': level, 'format': format }
    if file_path:
        kwargs['filename'] = file_path
    else:
        kwargs['stream'] = sys.stdout
    logging.basicConfig(**kwargs)
    return logging
