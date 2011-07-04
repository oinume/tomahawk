VERSION = '0.3.3'
DEFAULT_TIMEOUT = 10
DEFAULT_EXPECT_DELAY = 0.05
DEFAULT_EXPECT_ENCODING = 'utf-8'
DEFAULT_COMMAND_OUTPUT_FORMAT = '${user}@${host} % ${command}\n${output}\n'
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
