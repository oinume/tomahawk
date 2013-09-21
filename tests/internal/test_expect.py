from six.moves import StringIO

from flexmock import flexmock
import pexpect
import pytest
import utils
utils.append_home_to_path(__file__)

from tomahawk.expect import CommandWithExpect
from tomahawk.constants import TimeoutError

def test_00_execute():
    """Normal"""
    expect_out = StringIO()
    target = create_object(expect_out)
    expect_out.write("hello world\n")
    expect_out.write("Connection to localhost closed\n")

    status, output = target.execute()
    assert status == 0
    assert output == "hello world"

def test_01_execute_timeout():
    """Timeout"""
    target = create_object(StringIO())
    flexmock(utils.MockPexpect) \
        .should_receive('expect') \
        .and_raise(pexpect.TIMEOUT, "Timed out")
    pytest.raises(TimeoutError, target.execute)

def create_object(expect_out):
    command = 'ssh'
    command_args = [ '-t' ]
    expect = utils.MockPexpect(
        command, command_args, logfile = expect_out
    )
    return CommandWithExpect(
        command, command_args, 'password1', 'password2', debug_enabled = True,
        expect = expect, expect_out = expect_out
    )

