import argparse
import cStringIO
import os
import sys

def get_home_dir(file):
    abspath = os.path.abspath(file)
    parent, dir = None, None
    for dir in ( 'internal', 'internal2', 'external' ):
        if abspath.find(dir) != -1:
            return os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(file))))[0]
    return os.path.split(os.path.dirname(os.path.abspath(file)))[0]

def get_bin_dir(file):
    return os.path.join(get_home_dir(file), 'bin')

def append_home_to_path(file):
    sys.path.insert(0, get_home_dir(file))

def create_command_namespace(**kwargs):
    defaults = {
        'command': [ '' ], 'continue_on_error': None,
        'debug': False, 'deep_debug': False,
        'delay': 0, 'expect_delay': 0.1,
        'output_file': None, 'hosts': 'localhost', 'profile': False,
        'ssh_user': 'tomahawk',  'timeout': 10
    }
    for k, v in defaults.iteritems():
        kwargs.setdefault(k, v)
    return argparse.Namespace(**kwargs)

append_home_to_path(__file__)
from tomahawk.expect import CommandWithExpect
from tomahawk.constants import (
    DEFAULT_TIMEOUT,
    DEFAULT_EXPECT_DELAY
)

class StdoutCapture(object):
    def __init__(self):
        self.captured = cStringIO.StringIO()

    def start(self):
        sys.stdout = self.captured
        return self

    def stop(self):
        sys.stdout = sys.__stdout__
        return self

    def captured_value(self):
        return self.captured.getvalue()

    def close(self):
        self.captured.close()

class StderrCapture(StdoutCapture):
    def __init__(self):
        super(StderrCapture, self).__init__()

    def start(self):
        sys.stderr = self.captured
        return self

    def stop(self):
        sys.stderr = sys.__stderr__
        return self

class MockPexpect(object):
    def __init__(
        self, command, args = [], timeout = 30, maxread = 2000,
        searchwindowsize = None, logfile = None, cwd = None, env = None
    ):
        self.command = command
        self.args = args
        self.timeout = timeout
        self.maxread = maxread
        self.searchwindowsize = searchwindowsize
        self.logfile = logfile
        self.cwd = cwd
        self.env = env
        self._exitstatus = 0

    def expect(self, pattern, timeout = -1, searchwindowsize = -1):
        #sys.stdout.write("password: ")
        return 0

    def sendline(self, s = ''):
        if self.logfile:
            self.logfile.write(s + '\n')
        pass

    def send(self, s):
        pass

    def close(self):
        pass

    def get_exitstatus(self):
        return self._exitstatus

    def set_exitstatus(self, exitstatus):
        self._exitstatus = exitstatus

    exitstatus = property(get_exitstatus, set_exitstatus)

class MockCommandWithExpect(CommandWithExpect):
    def __init__(
        self, command, command_args, login_password, sudo_password,
        timeout = DEFAULT_TIMEOUT, expect_delay = DEFAULT_EXPECT_DELAY,
        debug_enabled = False, expect = None,
        expect_out = cStringIO.StringIO()
    ):
        if expect is None:
            expect = MockPexpect(command, command_args, timeout)
        super(MockCommandWithExpect, self).__init__(
            command, command_args, login_password, sudo_password,
            timeout, expect_delay, debug_enabled, expect, expect_out
        )

    def execute(self):
        return 0, ''
