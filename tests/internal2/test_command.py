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
    stdout = utils.StdoutCapture()
    stdout.start()

    def mock_parse_args(self):
        return utils.create_command_namespace(command = [ EXPECTED['command'] ])
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return EXPECTED['exit_status'], EXPECTED['command_output']
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    status = main.run()
    o = stdout.stop().captured_value()

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
    stderr = utils.StderrCapture()
    stderr.start()

    def mock_parse_args(self):
        return utils.create_command_namespace(command = [ EXPECTED['command'] ])
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return EXPECTED['exit_status'], "/bin/sh: command_not_found: command not found"
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    status = main.run()
    err = stderr.stop().captured_value()

    assert status == 1
    assert re.search(r'failed on host', err)

def test_02_run_timeout(monkeypatch):
    EXPECTED = {
        'command': 'sleep 3',
        'command_output': "/bin/sh: command_not_found: command not found",
    }
    stderr = utils.StderrCapture()
    stderr.start()

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
    err = stderr.stop().captured_value()
    assert status == 1
    assert re.search(r'timed out on host', err)

def test_03_run_option_host_files(monkeypatch):
    EXPECTED = {
        'command': 'echo "hello world"',
        'command_output': "hello world",
    }
    stdout = utils.StdoutCapture()
    stdout.start()

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
    out = stdout.stop().captured_value()
    assert status == 0
    assert re.search(r'hello world', out)

def test_04_run_option_continue_on_error(monkeypatch):
    EXPECTED = {
        'command': 'failure_command',
        'command_output': "hello world",
    }
    stderr = utils.StderrCapture()
    stderr.start()

    def mock_parse_args(self):
        return utils.create_command_namespace(
            command = [ EXPECTED['command'] ],
            continue_on_error = True,
            hosts = 'localhost,localhost',
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return 127, EXPECTED['command_output']
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    status = main.run()
    err = stderr.stop().captured_value()
    assert status == 1
    assert len(err.split('\n')) == 4

def test_05_execute_option_paralle_continue_on_error():
    pass

