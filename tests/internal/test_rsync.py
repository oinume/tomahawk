import cStringIO
import os
import re
from nose.tools import eq_, ok_

from tomahawk.base import BaseMain
from tomahawk.rsync import RsyncContext, RsyncExecutor, RsyncMain
from tomahawk.log import create_logger
from tomahawk.utils import check_hosts, get_home_dir

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = os.path.join(get_home_dir(__file__), 'tmp')
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

def test_01_execute():
    out, err = create_out_and_err()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost', hello_file, hello_file_copied ]
    )
    status = executor.execute(context.source, context.destination)
    eq_(0, status, "execute() > status")
    ok_(os.path.exists(hello_file_copied), "execute() > rsync copy")

def test_02_execute_error():
    out, err = create_out_and_err()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost', 'file_does_not_exist', TMP_DIR ]
    )
    status = executor.execute('file_does_not_exist', TMP_DIR)
    eq_(1, status, "execute() > error > status")
    ok_(not os.path.exists(os.path.join(TMP_DIR, 'file_does_not_exist')),
        "execute() > error > rsync failure")

def test_03_execute_timeout():
    out, err = create_out_and_err()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost', '--timeout=1', '--rsync-options=-av --dry-run', '/usr', TMP_DIR ]
    )
    status = executor.execute(context.source, context.destination)
    eq_(1, status, "execute() > timeout > status")
    ok_(re.search(r'timed out on host', err.getvalue()), "execute() > timeout > output")

def test_04_execute_option_rsync_options():
    hello_file_dry_run = os.path.join(TMP_DIR, 'hello.dry-run')
    out, err = create_out_and_err()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost', '--rsync-options=-av --dry-run',
          hello_file, hello_file_dry_run ]
    )
    status = executor.execute(context.source, context.destination)
    eq_(0, status, "execute() > option > --rsync-options > status")
    ok_(not os.path.exists(hello_file_dry_run),
        "execute() > option > --rsync-options > --dry-run file not copied")

def test_05_execute_option_mirror_mode_pull():
    target_files = ( 'localhost__hello', '127.0.0.1__hello' )
    for f in target_files:
        path = os.path.join(TMP_DIR, f)
        if os.path.exists(path):
            os.remove(path)
    out, err = create_out_and_err()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost,127.0.0.1', '--mirror-mode=pull',
          hello_file, TMP_DIR ]
    )
    status = executor.execute(context.source, context.destination)
    eq_(0, status, "execute() > option > --mirror-mode=pull > status")
    for f in target_files:
        ok_(os.path.exists(os.path.join(TMP_DIR, f)),
            "execute() > option > --mirror-mode=pull > %s exists" % (f))


def test_06_execute_option_continue_on_error():
    # without --continue-on-error
    out, err = create_out_and_err()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost,localhost', 'file_does_not_exist', TMP_DIR ]
    )
    executor.execute(context.source, context.destination)

    # with --continue-on-error
    out_continue, err_continue = create_out_and_err()
    context_continue, executor_continue = create_context_and_executor(
        out_continue, err_continue,
        [ '--hosts=localhost,localhost', '--continue-on-error',
          'file_does_not_exist', TMP_DIR ]
    )
    status_continue = executor_continue.execute(context.source, context.destination)
    eq_(1, status_continue, "execute() > option > --continue-on-error > status")

    # err_continue's length must be longer because the command continues even when error
    ok_(
        len(err_continue.getvalue()) > len(err.getvalue()),
        "execute > option > --continue-on-error > output"
    )

#    target_hosts = [
#        'localhost', 'localhost', 'localhost', 'localhost',
#        '127.0.0.1', '127.0.0.1', '127.0.0.1', '127.0.0.1',
#    ]
#    out_order, err_order = create_out_and_err()
#    context_order, executor_order = create_context_and_executor(
#        out_order, err_order,
#        [ '--hosts=%s' % (','.join(target_hosts)),
#          'failure_command', '--continue-on-error', '--parallel=2' ]
#    )
#    status_order = executor_order.execute(context_order.arguments)
#    eq_(1, status_order, "execute() > option > --continue-on-error, --parallel > status")
#
#    # parse output to collect failure hosts.
#    hosts = []
#    hosts_start = False
#    for line in err_order.getvalue().split('\n'):
#        if re.search(r'failed on following hosts', line, re.I):
#            hosts_start = True
#            continue
#        if hosts_start:
#            h = line.strip()
#            if h != '':
#                hosts.append(h)
#
#    eq_(hosts, target_hosts, "execute > option > --continue-on-error > error hosts order")

def create_out_and_err():
    return cStringIO.StringIO(), cStringIO.StringIO()

def create_context_and_executor(out, err, args):
    arg_parser = create_rsync_argument_parser(__file__)
    log = create_logger(True)
    options = arg_parser.parse_args(args)
    context = RsyncContext(options.source, options.destination, options.__dict__, out, err)
    hosts = check_hosts(options.__dict__, log, arg_parser.format_usage)
    return context, RsyncExecutor(context, log, hosts)

def create_rsync_argument_parser(file):
    parser = RsyncMain.create_argument_parser(file)
    BaseMain.add_common_arguments(parser)
    return parser
