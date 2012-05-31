import argparse
import os
import re
import shutil
import utils

utils.append_home_to_path(__file__)

from tomahawk.rsync import RsyncMain
from tomahawk.constants import TimeoutError
from tomahawk.expect import CommandWithExpect

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = os.path.join(utils.get_home_dir(__file__), 'tmp')
if not os.path.exists(TMP_DIR):
    os.mkdir(TMP_DIR)

env = os.environ
if env.get('TOMAHAWK_ENV') != None:
    del env['TOMAHAWK_ENV']

hello_file = os.path.join(TMP_DIR, 'hello')
hello_file_copied = os.path.join(TMP_DIR, 'hello.copied')
if os.path.exists(hello_file_copied):
    os.remove(hello_file_copied)
handle = open(hello_file, 'w')
handle.write('hello world')
handle.close()

def test_00_run(monkeypatch):
    EXPECTED = {
        'exit_status': 0,
    }
    stdout, stderr = utils.capture_stdout_stderr()

    def mock_parse_args(self):
        return utils.create_rsync_namespace(
            source = hello_file,
            destination = hello_file_copied,
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        shutil.copyfile(hello_file, hello_file_copied)
        return EXPECTED['exit_status'], ''
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = RsyncMain('tomahawk-rsync')
    status = main.run()
    assert status == EXPECTED['exit_status']
    assert os.path.exists(hello_file_copied)

def test_01_run_error(monkeypatch):
    EXPECTED = {
        'exit_status': 1,
    }
    stdout, stderr = utils.capture_stdout_stderr()

    def mock_parse_args(self):
        return utils.create_rsync_namespace(
            source = 'file_does_not_exist',
            destination = TMP_DIR,
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        shutil.copyfile(hello_file, hello_file_copied)
        return EXPECTED['exit_status'], ''
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = RsyncMain('tomahawk-rsync')
    status = main.run()
    assert status == 1
    assert not os.path.exists(os.path.join(TMP_DIR, 'file_does_not_exist'))

def test_02_run_timeout(monkeypatch):
    EXPECTED = {
        'exit_status': 1,
    }
    stdout, stderr = utils.capture_stdout_stderr()

    def mock_parse_args(self):
        return utils.create_rsync_namespace(
            source = 'file_does_not_exist',
            destination = TMP_DIR,
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        raise TimeoutError()
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = RsyncMain('tomahawk-rsync')
    status = main.run()
    err = stderr.stop().value()
    assert status == EXPECTED['exit_status']
    assert re.search(r'timed out on host', err)

def test_10_run_option_rsync_options(monkeypatch):
    EXPECTED = {
        'exit_status': 0,
    }
    stdout, stderr = utils.capture_stdout_stderr()
    hello_file_dry_run = os.path.join(TMP_DIR, 'hello.dry-run')

    def mock_parse_args(self):
        return utils.create_rsync_namespace(
            source = hello_file,
            destination = hello_file_copied,
            rsync_options = '-av --dry-run',
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return EXPECTED['exit_status'], ''
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = RsyncMain('tomahawk-rsync')
    status = main.run()
    assert status == EXPECTED['exit_status']
    assert not os.path.exists(hello_file_dry_run)

def test_11_run_option_mirror_mode_pull(monkeypatch):
    EXPECTED = {
        'exit_status': 0,
    }
    stdout, stderr = utils.capture_stdout_stderr()
    target_files = ( 'localhost__hello', '127.0.0.1__hello' )
    # remove target_files
    for f in target_files:
        path = os.path.join(TMP_DIR, f)
        if os.path.exists(path):
            os.remove(path)

    def mock_parse_args(self):
        return utils.create_rsync_namespace(
            source = hello_file,
            destination = TMP_DIR,
            hosts = 'localhost,127.0.0.1',
            mirror_mode = 'pull',
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        for f in target_files:
            shutil.copyfile(hello_file, os.path.join(TMP_DIR, f))
        return EXPECTED['exit_status'], ''
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = RsyncMain('tomahawk-rsync')
    status = main.run()
    assert status == EXPECTED['exit_status']
    for f in target_files:
        assert os.path.exists(os.path.join(TMP_DIR, f))

def test_21_run_option_continue_on_error(monkeypatch):
    EXPECTED = {
        'exit_status': 1,
    }
    stdout, stderr = utils.capture_stdout_stderr()

    def mock_parse_args(self):
        return utils.create_rsync_namespace(
            source = hello_file,
            destination = TMP_DIR,
            hosts = 'localhost,127.0.0.1',
            continue_on_error = True,
        )
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return 127, 'error when rsync'
    monkeypatch.setattr(CommandWithExpect, 'execute', mock_execute)

    main = RsyncMain('tomahawk-rsync')
    status = main.run()
    err = stderr.stop().value()
    assert status == EXPECTED['exit_status']
    assert len(err.split('\n')) == 4
