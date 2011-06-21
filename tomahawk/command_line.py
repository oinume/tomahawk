# -*- coding: utf-8 -*-
__all__ = ("CommandContext", "RsyncContext")

class BaseContext(object):
    pass

class CommandContext(BaseContext):
    """
    """
    def __init__(self, arguments, options):
        self.arguments = arguments
        self.options = options

class RsyncContext(BaseContext):
    """
    """
    def __init__(self, source, destination, options):
        self.source = source
        self.destination = destination
        self.options = options

