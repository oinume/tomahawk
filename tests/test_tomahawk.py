from nose.tools import assert_equal, ok_
import os
import pexpect
from subprocess import call, PIPE, Popen
import sys
import utils

TOMAHAWK_PATH = os.path.join(utils.get_bin_dir(__file__), 'tomahawk')
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
MOCK_SSH_PATH = os.path.join(TESTS_DIR, 'mock_ssh.py')

#def test_00_ssh():
#    status = call(
#        [ TOMAHAWK_PATH, '--hosts=localhost,localhost', '--ssh=' + MOCK_SSH_PATH, 'uptime' ],
#        stdout = PIPE, stderr = PIPE
#    )
#    assert_equal(status, 0, 'execute (mock_ssh)')

def test_01_basic():
    status = call(
        [ TOMAHAWK_PATH, '--hosts=localhost,localhost', 'uptime' ],
#        stdout = PIPE, stderr = PIPE
    )
    assert_equal(status, 0, 'execute (basic)')

def test_02_hosts_files():
    hosts_files = os.path.join(TESTS_DIR, 'localhost_2.hosts')
    status = call(
        [ TOMAHAWK_PATH, '--hosts-files=' + hosts_files, 'uptime' ],
#        stdout = PIPE, stderr = PIPE
    )
    assert_equal(status, 0, 'execute (--hosts-files)')

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
    ok_(len(error_c) > len(error), 'execute (--continue-on-error)')

def test_04_ssh_options():
    status = call(
        [ TOMAHAWK_PATH, '--hosts=localhost,localhost', "--ssh-options=-c arcfour", 'uptime' ],
#        stdout = PIPE, stderr = PIPE
    )
    assert_equal(status, 0, 'execute (--ssh-options)')

def test_05_confirm_execution_on_production():
    command = TOMAHAWK_PATH + ' --hosts=localhost,localhost uptime'
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
