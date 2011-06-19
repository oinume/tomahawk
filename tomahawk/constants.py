VERSION = '0.3.2'
DEFAULT_TIMEOUT = 10
DEFAULT_EXPECT_DELAY = 0.05
DEFAULT_EXPECT_ENCODING = 'utf-8'
DEFAULT_RSYNC_OPTIONS = '-av'

# TODO: should rename to tomahawk_common ?
class TimeoutError(RuntimeError):
    """Timeout error of command execution."""
    pass

class CommandError(RuntimeError):
    """Command execution error."""
    pass

class FatalError(RuntimeError):
    """A fatal error in tomahawk."""
    pass
