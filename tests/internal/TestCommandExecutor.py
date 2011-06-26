import cStringIO
import os
import re
from nose.tools import assert_equal, eq_, ok_

from tomahawk.base import BaseMain
from tomahawk.command import CommandContext, CommandExecutor, CommandMain
from tomahawk.log import create_logger
from tomahawk.utils import check_hosts

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

def test_01_execute():
    out, err = create_out_and_err()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost', 'echo "hello world!"' ]
    )
    status = executor.execute(context.arguments)
    eq_(0, status, "execute(): status")
    ok_(re.search(r'hello world', out.getvalue()), "execute(): output")

def test_02_execute_option_host_files():
    out, err = create_out_and_err()
    hosts_files = os.path.join(TESTS_DIR, 'localhost_2.hosts')
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts-files=' + hosts_files, 'echo "hello world!"' ]
    )
    status = executor.execute(context.arguments)
    eq_(0, status, "execute(): --hosts-files: status")
    ok_(re.search(r'hello world', out.getvalue()), "execute(): --hosts-files: output")

def test_03_execute_option_continue_on_error():
    out, err = create_out_and_err()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost,localhost', 'no_such_command' ]
    )
    # TODO: test_tomahawk.py -c

def create_out_and_err():
    return cStringIO.StringIO(), cStringIO.StringIO()

def create_context_and_executor(out, err, args):
    arg_parser = create_command_argument_parser(__file__)
    log = create_logger(True)
    options = arg_parser.parse_args(args)
    context = CommandContext(options.command, options.__dict__, out, err)
    hosts = check_hosts(options.__dict__, log, arg_parser.format_usage)
    return context, CommandExecutor(context, log, hosts)

def create_command_argument_parser(file):
    parser = CommandMain.create_argument_parser(file)
    BaseMain.add_common_arguments(parser)
    return parser
