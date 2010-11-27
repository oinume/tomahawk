from nose.tools import assert_equal, assert_true
import os
from subprocess import call, PIPE, Popen
import utils

TOMAHAWK_PATH = os.path.join(utils.get_bin_dir(__file__), 'tomahawk.py')

def test_basic():
    status = call(
        [ TOMAHAWK_PATH, '--hosts=localhost,localhost', 'uptime' ],
        stdout = PIPE, stderr = PIPE
    )
    assert_equal(status, 0, 'execute (basic)')

def test_continue_on_error():
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
