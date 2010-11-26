import logging

def create_logger(debug_enabled=False):
    logging.basicConfig(
        level = logging.DEBUG if debug_enabled else logging.INFO,
        format = '[%(levelname)s] %(message)s'
    )
    return logging
