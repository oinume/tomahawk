#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pexpect
import os
#/Users/kazuhiro/work/tomahawk/tests/bin/mock_ssh.py', '--prompt=Password: ', '-l', 'kazuhiro', 'localhost', "/bin/sh -c 'uptime'"
dir = os.path.dirname(os.path.abspath(__file__))
program = os.path.join(dir, 'mock_ssh.py')
program_with_options = program + " --prompt='Password: ' -l kazuhiro localhost \"/bin/sh -c 'uptime'\""
child = pexpect.spawn(
    program_with_options,
#    [ '--prompt=Password: ', '-l', 'kazuhiro', 'localhost', "/bin/sh -c 'uptime'" ],
    timeout = 5
)

try:
    index = child.expect([ 'Password: ' ])
    if index == 0:
        print "OK"
        child.sendline('send test')
    else:
        print "NG"
except pexpect.EOF:
    print "EOF"
except pexpect.TIMEOUT:
    print "TIMEOUT"
