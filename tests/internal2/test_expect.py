import os
import sys
from mock import Mock, patch
import cStringIO

sys.path.insert(0, os.path.abspath('.'))

print sys.path

import tomahawk.expect

def test_00_execute():
    out = cStringIO.StringIO()
    out.flush()
    target = create_object(out)
    out.write("hogehoge")
    status, output = target.execute()
    assert 1 == 'fuga'

def create_object(logfile):
    return tomahawk.expect.CommandWithExpect(
        'ssh', [ '-t' ], 'hoge', 'hoge',
        debug_enabled=True, expect=MockPexpect)

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
        self._exitstatus = None

    def expect(self, pattern, timeout = -1, searchwindowsize = -1):
        return 0

    def sendline(self, s = ''):
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
