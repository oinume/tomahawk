#!/usr/bin/env python
# -*- coding: utf-8 -*-

from six import print_
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
        print_('OK')
        child.sendline('send test')
    else:
        print_('NG')
except pexpect.EOF:
    print_('EOF')
except pexpect.TIMEOUT:
    print_('TIMEOUT')
