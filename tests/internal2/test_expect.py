import cStringIO
from mock import Mock
import os
import pexpect
import pytest
import sys

sys.path.insert(0, os.path.abspath('.'))

print sys.path

import tomahawk.expect
import tomahawk.constants

def test_00_execute():
    expect_out = cStringIO.StringIO()
    target = create_object(expect_out)
    expect_out.write("hello world\n")
    expect_out.write("Connection to localhost closed\n")

    status, output = target.execute()
    assert(status == 0)
    assert(output == "hello world")

def test_01_execute_timeout():
    target = create_object(cStringIO.StringIO())
    MockPexpect.expect = Mock(side_effect = pexpect.TIMEOUT('timeout'))
    pytest.raises(tomahawk.constants.TimeoutError, target.execute)

def create_object(expect_out):
    command = 'ssh'
    command_args = [ '-t' ]
    expect = MockPexpect(
        command, command_args, logfile = expect_out
    )
    return tomahawk.expect.CommandWithExpect(
        command, command_args, 'password1', 'password2', debug_enabled = True,
        expect = expect, expect_out = expect_out
    )

class MockPexpect(object):
    def __init__(
        self, command, args = [], timeout = 30, maxread = 2000,
        searchwindowsize = None, logfile = None, cwd = None, env = None):
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
