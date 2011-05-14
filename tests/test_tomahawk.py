# -*- coding: utf-8 -*-
from nose.tools import assert_equal, eq_, ok_
import os
import re
import pexpect
from subprocess import call, PIPE, Popen
#import sys
import utils

# TODO: mock_ssh.py --prompt enabled, so we can test -s -l options.
TOMAHAWK_PATH = os.path.join(utils.get_bin_dir(__file__), 'tomahawk')
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

def test_01_basic():
    status = call(
        [ TOMAHAWK_PATH, '--hosts=localhost,localhost', 'uptime' ],
#        stdout = PIPE, stderr = PIPE
    )
    eq_(status, 0, 'execute (basic)')

    status = call(
        [ TOMAHAWK_PATH, '--continue-on-error', '--parallel=2',
          '--hosts=localhost,localhost,localhost,localhost,127.0.0.1,127.0.0.1,127.0.0.1,127.0.0.1', 'hoge' ],
#        stdout = PIPE, stderr = PIPE
    )


##########################
# options
#########################

def test_02_hosts_files():
    hosts_files = os.path.join(TESTS_DIR, 'localhost_2.hosts')
    status = call(
        [ TOMAHAWK_PATH, '--hosts-files=' + hosts_files, 'uptime' ],
#        stdout = PIPE, stderr = PIPE
    )
    assert_equal(status, 0, "execute (--hosts-files)")

def test_03_continue_on_error():
    p = Popen(
        [ TOMAHAWK_PATH, '--hosts=localhost,localhost', 'doesnotexist' ],
        stdout = PIPE, stderr = PIPE
    )
    out, error = p.communicate()

    p_with_c = Popen(
        [ TOMAHAWK_PATH, '--hosts=localhost,localhost', '-c', 'doesnotexist' ],
        stdout = PIPE, stderr = PIPE
    )
    out_c, error_c = p_with_c.communicate()
    # error_c's length must be longer because the command continues even when error
    ok_(len(error_c) > len(error), "execute (--continue-on-error)")

    target_hosts = [
        'localhost', 'localhost', 'localhost', 'localhost',
        '127.0.0.1', '127.0.0.1', '127.0.0.1', '127.0.0.1',
    ]
    p = Popen(
        [ TOMAHAWK_PATH, '--continue-on-error', '--parallel=2',
          '--hosts=%s' % (','.join(target_hosts)),
          'doescnotexist'
        ],
        stdout = PIPE, stderr = PIPE
    )
    out, error = p.communicate()

    # parse output to collect failure hosts.
    hosts = []
    hosts_start = False
    for line in error.split('\n'):
        if re.search(r'failed on following hosts', line, re.I):
            hosts_start = True
            continue
        if hosts_start:
            h = line.strip()
            if h != '':
                hosts.append(h)

    eq_(hosts, target_hosts, "execute (--continue-on-error: error hosts order)")

# TODO: ssh_options should be deprecated.
def test_04_ssh_options():
    status = call(
        [ TOMAHAWK_PATH, "--hosts=localhost,localhost", "--ssh-options=-c arcfour", 'uptime' ],
#        stdout = PIPE, stderr = PIPE
    )
    assert_equal(status, 0, "execute (--ssh-options)")

def test_05_timeout():
    status = call(
        [ TOMAHAWK_PATH, "--hosts=localhost", "--timeout=5", 'sleep 2' ],
#        stdout = PIPE, stderr = PIPE
    )
    assert_equal(status, 0, "execute (--timeout)")

    process = Popen(
        [ TOMAHAWK_PATH, "--hosts=localhost", "--timeout=1", 'sleep 3' ],
        stdout = PIPE, stderr = PIPE
    )
    out, error = process.communicate()
    ok_(re.search(r'timed out', error) , "execute (--timeout: output)")

    # TODO: with -c

def test_06_prompt_sudo_password():
    command = "%s --hosts=localhost --prompt-login-password --ssh-user=tomahawk_test uptime" % (TOMAHAWK_PATH)
    child = pexpect.spawn(
        command,
        timeout = 5
    )
    i = child.expect([ pexpect.EOF, pexpect.TIMEOUT, 'Enter a password.+' ])
    if i == 0: # EOF
        print 'EOF'
        print child.before
    elif i == 1: # timeout
        print 'TIMEOUT'
        #print child.before, child.after
        ok_(False, 'Failure: ')
    elif i == 2:
        child.sendline("tomahawk_test")
        child.expect(pexpect.EOF)
        #print child.before
        ok_(True, "execute (prompt password)")


def test_10_confirm_execution_on_production():
    command = '%s --hosts=localhost,localhost uptime' % (TOMAHAWK_PATH)
    env = os.environ
    env['TOMAHAWK_ENV'] = 'production'
    child = pexpect.spawn(
        command,
        timeout = 5,
#        logfile = sys.stdout,
        env = env
    )
    i = child.expect([ pexpect.EOF, pexpect.TIMEOUT, 'Command "uptime" will be executed to 2 hosts.' ])
    if i == 0: # EOF
        print 'EOF'
        print child.before
    elif i == 1: # timeout
        print 'TIMEOUT'
        print child.before, child.after
        ok_(False, 'Failure: confirm_execution_on_production with "TOMAHAWK_ENV"')
    elif i == 2:
        child.sendline('yes')
        child.expect(pexpect.EOF)
        print child.before
        ok_(True, 'confirm_execution_on_production with "TOMAHAWK_ENV"')
