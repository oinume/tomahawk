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
    status = executor.execute(hello_file, hello_file_copied)
    eq_(0, status, "execute() > status")
    ok_(os.path.exists(hello_file_copied), "execute() > rsync copy")

def test_02_execute_option_rsync_options():
    hello_file_dry_run = os.path.join(TMP_DIR, 'hello.dry-run')
    out, err = create_out_and_err()
    context, executor = create_context_and_executor(
        out, err,
        [ '--hosts=localhost', '--rsync-options=-av --dry-run',
          hello_file, hello_file_dry_run ]
    )
    status = executor.execute(hello_file, hello_file_dry_run)
    eq_(0, status, "execute() > option > --rsync-options > status")
    ok_(not os.path.exists(hello_file_dry_run),
        "execute() > option > --rsync-options > --dry-run file not copied")

def test_03_execute_option_mirror_mode_pull():
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
    status = executor.execute(hello_file, TMP_DIR)
    eq_(0, status, "execute() > option > --mirror-mode=pull > status")
    for f in target_files:
        #print os.path.exists(os.path.join(TMP_DIR, f))
        ok_(os.path.exists(os.path.join(TMP_DIR, f)),
            "execute() > option > --mirror-mode=pull > %s exists" % (f))


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
