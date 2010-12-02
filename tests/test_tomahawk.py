from nose.tools import assert_equal, assert_true
import os
from subprocess import call, PIPE, Popen
import utils

TOMAHAWK_PATH = os.path.join(utils.get_bin_dir(__file__), 'tomahawk')
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

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
    assert_true(len(error_c) > len(error), 'execute (--continue-on-error)')

def test_04_ssh_options():
    status = call(
        [ TOMAHAWK_PATH, '--hosts=localhost,localhost', "--ssh-options=-c arcfour", 'uptime' ],
#        stdout = PIPE, stderr = PIPE
    )
    assert_equal(status, 0, 'execute (--ssh-options)')
