from tomahawk.base import BaseMain
from tomahawk.command import CommandContext, CommandExecutor, CommandMain
from tomahawk.log import create_logger
from tomahawk.utils import check_hosts
import cStringIO
import re
from nose.tools import assert_equal, eq_, ok_

def test_execute():
    out = cStringIO.StringIO()
    err = cStringIO.StringIO()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost', 'echo "hello world!"' ]
    )
    status = executor.execute(context.arguments)
    eq_(0, status, "status")
    ok_(re.search(r'hello world', out.getvalue()), "hello world string")

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
