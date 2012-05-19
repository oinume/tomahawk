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
    assert status == 0
    assert os.path.exists(hello_file_copied)
