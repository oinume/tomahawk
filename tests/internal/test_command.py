import cStringIO
import os
import re
from nose.tools import eq_, ok_

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
    eq_(0, status, "execute() > status")
    ok_(re.search(r'hello world', out.getvalue()), "execute() > output")

def test_02_execute_error():
    out, err = create_out_and_err()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost', 'failure_command' ]
    )
    status = executor.execute(context.arguments)
    eq_(1, status, "execute() > error > status")
    ok_(re.search(r'failed on host', err.getvalue()), "execute() > error > output")

def test_03_execute_timeout():
    out, err = create_out_and_err()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost', '--timeout=1', 'sleep 5' ]
    )
    status = executor.execute(context.arguments)
    eq_(1, status, "execute() > timeout > status")
    ok_(re.search(r'timed out on host', err.getvalue()), "execute() > timeout > output")

def test_04_execute_option_host_files():
    out, err = create_out_and_err()
    hosts_files = os.path.join(TESTS_DIR, 'localhost_2.hosts')
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts-files=' + hosts_files, 'echo "hello world!"' ]
    )
    status = executor.execute(context.arguments)
    eq_(0, status, "execute() > option > --hosts-files > status")
    ok_(re.search(r'hello world', out.getvalue()), "execute() > option > --hosts-files > output")

def test_05_execute_option_continue_on_error():
    # without --continue-on-error
    out, err = create_out_and_err()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost,localhost', 'failure_command' ]
    )
    executor.execute(context.arguments)

    # with --continue-on-error
    out_continue, err_continue = create_out_and_err()
    context_continue, executor_continue = create_context_and_executor(
        out_continue, err_continue,
        [ '--hosts=localhost,localhost', '--continue-on-error', 'failure_command' ]
    )
    status_continue = executor_continue.execute(context_continue.arguments)
    eq_(1, status_continue, "execute() > option > --continue-on-error > status")

    # err_continue's length must be longer because the command continues even when error
    ok_(
        len(err_continue.getvalue()) > len(err.getvalue()),
        "execute > option > --continue-on-error > output"
    )

    target_hosts = [
        'localhost', 'localhost', 'localhost', 'localhost',
        '127.0.0.1', '127.0.0.1', '127.0.0.1', '127.0.0.1',
    ]
    out_order, err_order = create_out_and_err()
    context_order, executor_order = create_context_and_executor(
        out_order, err_order,
        [ '--hosts=%s' % (','.join(target_hosts)),
          'failure_command', '--continue-on-error', '--parallel=2' ]
    )
    status_order = executor_order.execute(context_order.arguments)
    eq_(1, status_order, "execute() > option > --continue-on-error, --parallel > status")

    # parse output to collect failure hosts.
    hosts = []
    hosts_start = False
    for line in err_order.getvalue().split('\n'):
        if re.search(r'failed on following hosts', line, re.I):
            hosts_start = True
            continue
        if hosts_start:
            h = line.strip()
            if h != '':
                hosts.append(h)

    eq_(hosts, target_hosts, "execute > option > --continue-on-error > error hosts order")

def test_06_execute_option_ssh_options():
    out, err = create_out_and_err()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost', '-D', "--ssh-options=-o LogLevel=debug", 'uptime' ]
    )
    status = executor.execute(context.arguments)
    eq_(0, status, "execute() > option > --ssh-options > status")
    ok_(re.search(r'debug1: Exit status 0', out.getvalue()), "execute() > option > --ssh-options > output")


def test_07_output_format():
    out, err = create_out_and_err()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost', r"--output-format='${host} @ ${command}'", 'uptime' ]
    )
    status = executor.execute(context.arguments)
    eq_(0, status, "execute() > option > --output-format > status")
    ok_(
        re.search(r'localhost @ uptime', out.getvalue()) ,
        "execute() > option > --output-format > output"
    )

    # \n new line test
    out2, err2 = create_out_and_err()
    context, executor = create_context_and_executor(
        out2, err2,
        [ '--hosts=localhost', r"--output-format='${host} @ ${command}\noutput:${output}'", 'uptime' ]
    )
    status2 = executor.execute(context.arguments)
    eq_(0, status2, "execute() > option > --output-format > newline > status")
    ok_(
        re.search(r'localhost @ uptime', out2.getvalue()) ,
        "execute() > option > --output-format > newline > output"
    )

    # \\n no new line test
    out3, err3 = create_out_and_err()
    context, executor = create_context_and_executor(
        out3, err3,
        [ '--hosts=localhost', r"--output-format='${command} \\n output:${output}'", 'uptime' ]
    )
    status3 = executor.execute(context.arguments)
    eq_(0, status3, "execute() > option > --output-format > no newline > status")
    ok_(
        re.search(r'uptime \\\\n output:', out3.getvalue()) ,
        "execute() > option > --output-format > no newline > output"
    )


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
