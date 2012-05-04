import argparse
from mock import Mock, patch
import pytest
import sys
import utils
utils.append_home_to_path(__file__)

import tomahawk.command

def test_00_run():
    parse_args_patch = patch('argparse.ArgumentParser.parse_args')
    parse_args_patch.start()
    argparse.ArgumentParser.parse_args.return_value = create_namespace('uptime')
    main = tomahawk.command.CommandMain('tomahawk')
    status = main.run()
    assert status == 1
    # TODO: Use MockPexpect

def create_namespace(command):
    n = argparse.Namespace(
        command = [ command ], continue_on_error = None,
        debug = True, deep_debug = True, delay = 0, expect_delay = 0.1,
        hosts = 'localhost',
        profile = False, timeout = 10,
    )
    return n
#Namespace(command=['uptime'], continue_on_error=None, debug=True, deep_debug=False, delay=0, expect_delay=0.050000000000000003, expect_encoding='utf-8', expect_timeout=None, hosts=None, hosts_files=None, login_password_stdin=False, no_sudo_password=False, output_format='${user}@${host} % ${command}\n${output}\n', parallel=1, profile=False, prompt_login_password=False, prompt_sudo_password=False, ssh='ssh', ssh_options=None, ssh_user=None, sudo_password_stdin=False, timeout=10)
