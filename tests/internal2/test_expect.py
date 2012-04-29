import os
import sys
import mock
import pexpect

sys.path.insert(0, os.path.abspath('.'))

print sys.path

import tomahawk.expect

def test_execute():
    target = create_object()
    
    p = mock.patch('pexpect.spawn.expect')
    #print "p = " + str(p)
    p.start()
    pexpect.spawn.expect.return_value = 0
    print "target = " + str(target)
    target.execute()
    assert 1 == 'fuga'

def create_object():
    return tomahawk.expect.CommandWithExpect('ssh', [ '-t' ], 'hoge', 'hoge', debug_enabled=True)
