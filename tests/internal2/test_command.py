import argparse
#import pytest
import utils
utils.append_home_to_path(__file__)

from tomahawk.command import CommandMain
import tomahawk.expect

def test_00_run(monkeypatch):
    def mock_parse_args(self):
        return utils.create_argparse_namespace(command = [ 'uptime' ])
    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    def mock_execute(self):
        return 0, "0:40  up 1 day,  8:19, 4 users, load averages: 0.00 0.50 1.00"
    monkeypatch.setattr(tomahawk.expect.CommandWithExpect, 'execute', mock_execute)

    main = CommandMain('tomahawk')
    status = main.run()
    assert status == 1

