import argparse
import re
import utils

utils.append_home_to_path(__file__)

from tomahawk.command import CommandMain
from tomahawk.constants import TimeoutError
from tomahawk.expect import CommandWithExpect

def test_00_run(monkeypatch):
    EXPECTED = {
        'command': 'uptime',
        'command_output': "0:40  up 1 day,  8:19, 4 users, load averages: 0.00 0.50 1.00",
        'exit_status': 0,
    }
    stdout, stderr = utils.capture_stdout_stderr()

    def mock_parse_args(self):
        return utils.create_command_namespace(command = [ EXPECTED['command'] ])
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return EXPECTED['exit_status'], EXPECTED['command_output']
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    status = main.run()
    o = stdout.stop().value()

    assert status == 0
    s = \
"""tomahawk@localhost %% %(command)s
%(command_output)s

""" % EXPECTED
    assert o == s

def test_01_run_error(monkeypatch):
    EXPECTED = {
        'command': 'command_not_found',
        'exit_status': 127,
    }
    stdout, stderr = utils.capture_stdout_stderr()

    def mock_parse_args(self):
        return utils.create_command_namespace(command = [ EXPECTED['command'] ])
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return EXPECTED['exit_status'], "/bin/sh: command_not_found: command not found"
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    status = main.run()
    assert status == 1
    assert re.search(r'failed on host', stderr.stop().value())

def test_02_run_timeout(monkeypatch):
    EXPECTED = {
        'command': 'sleep 3',
        'command_output': "/bin/sh: command_not_found: command not found",
    }
    stdout, stderr = utils.capture_stdout_stderr()

    def mock_parse_args(self):
        return utils.create_command_namespace(
            command = [ EXPECTED['command'] ], timeout = 1
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        raise TimeoutError()
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    status = main.run()
    assert status == 1
    assert re.search(r'timed out on host', stderr.stop().value())

def test_10_run_option_host_files(monkeypatch):
    EXPECTED = {
        'command': 'echo "hello world"',
        'command_output': "hello world",
    }
    stdout, stderr = utils.capture_stdout_stderr()

    def mock_parse_args(self):
        return utils.create_command_namespace(
            command = [ EXPECTED['command'] ],
            hosts = 'localhost,localhost',
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return 0, EXPECTED['command_output']
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    status = main.run()
    assert status == 0
    assert re.search(r'hello world', stdout.stop().value())

def test_20_run_option_continue_on_error(monkeypatch):
    EXPECTED = {
        'command': 'failure_command',
        'command_output': "hello world",
    }
    stdout, stderr = utils.capture_stdout_stderr()

    def mock_parse_args(self):
        return utils.create_command_namespace(
            command = [ EXPECTED['command'] ],
            continue_on_error = True,
            hosts = 'localhost,127.0.0.1',
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return 127, EXPECTED['command_output']
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    status = main.run()
    err = stderr.stop().value()
    assert status == 1
    assert len(err.split('\n')) == 4

def test_21_run_option_parallel_continue_on_error(monkeypatch):
    EXPECTED = {
        'command': 'failure_command',
        'command_output': "hello world",
    }
    stdout, stderr = utils.capture_stdout_stderr()
    target_hosts = [
        'localhost', 'localhost', 'localhost', 'localhost',
        '127.0.0.1', '127.0.0.1', '127.0.0.1', '127.0.0.1',
    ]
    def mock_parse_args(self):
        return utils.create_command_namespace(
            command = [ EXPECTED['command'] ],
            continue_on_error = True,
            parallel = 2,
            hosts = ','.join(target_hosts),
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return 127, EXPECTED['command_output']
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    status = main.run()
    assert status == 1

    # parse output to collect failure hosts.
    hosts = []
    hosts_start = False
    for line in stderr.stop().value().split('\n'):
        if re.search(r'failed on following hosts', line, re.I):
            hosts_start = True
            continue
        if hosts_start:
            h = line.strip()
            if h != '':
                hosts.append(h)
    assert hosts == target_hosts

def test_30_execute_option_ssh_options(monkeypatch):
    EXPECTED = {
        'command': 'echo "hello world"',
        'command_output': "hello world",
    }
    stdout, stderr = utils.capture_stdout_stderr()

    def mock_parse_args(self):
        return utils.create_command_namespace(
            command = [ EXPECTED['command'] ],
            ssh_options = '-c arcfour',
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return 0, EXPECTED['command_output']
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    status = main.run()
    assert status == 0
    assert re.search(EXPECTED['command_output'], stdout.stop().value())

def test_40_output_format(monkeypatch):
    EXPECTED = {
        'command': 'uptime',
        'command_output': r'localhost @ uptime',
    }
    stdout, stderr = utils.capture_stdout_stderr()

    def mock_parse_args(self):
        return utils.create_command_namespace(
            command = [ EXPECTED['command'] ],
            output_format = r'${host} @ ${command}',
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return 0, EXPECTED['command_output']
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    status = main.run()
    out = stdout.stop().value()
    assert status == 0
    assert EXPECTED['command_output'] == out.strip()

def test_41_output_format_newline(monkeypatch):
    """\n new line test"""
    EXPECTED = {
        'command': 'uptime',
        'command_output': "localhost\nuptime",
    }
    stdout, stderr = utils.capture_stdout_stderr()

    def mock_parse_args(self):
        return utils.create_command_namespace(
            command = [ EXPECTED['command'] ],
            output_format = r"${host}\n${command}",
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return 0, EXPECTED['command_output']
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    status = main.run()
    assert status == 0
    assert EXPECTED['command_output'] == stdout.stop().value().strip()

def test_42_output_format_no_newline(monkeypatch):
    """\\n no new line test"""
    EXPECTED = {
        'command': 'uptime',
        'command_output': r"localhost \\n uptime",
    }
    stdout, stderr = utils.capture_stdout_stderr()

    def mock_parse_args(self):
        return utils.create_command_namespace(
            command = [ EXPECTED['command'] ],
            output_format = r'${host} \\n ${command}',
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return 0, EXPECTED['command_output']
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    status = main.run()
    assert status == 0
    assert EXPECTED['command_output'] == stdout.stop().value().strip()

def test_50_parallel_adjustment(monkeypatch):
    stdout, stderr = utils.capture_stdout_stderr()

    def mock_parse_args(self):
        return utils.create_command_namespace(
            command = [ 'uptime' ], parallel = 10
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return 0, "mock execute"
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    main.run()
    assert main.context.options['parallel'] == 1

