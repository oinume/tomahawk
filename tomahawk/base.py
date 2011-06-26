# -*- coding: utf-8 -*-
import multiprocessing
import os
import sys

from tomahawk.constants import (
    VERSION,
    DEFAULT_TIMEOUT,
    DEFAULT_EXPECT_DELAY,
    DEFAULT_EXPECT_ENCODING,
)
from tomahawk.log import create_logger
from tomahawk.utils import (
    check_hosts,
    read_login_password,
    read_sudo_password,
)
class BaseContext(object):
    def __init__(self, options = {}, out = sys.stdout, err = sys.stderr):
        self.options = options
        self.out = out
        self.err = err

class BaseMain(object):
    def __init__(self, script_path):
        self.script_path = script_path
        self.arg_parser = self.create_argument_parser(file)
        self.options = self.arg_parser.parse_args()
        self.log = create_logger(self.options.debug)
    
#    def initialize(self, script_path, arg_parser):
#        self.script_path = script_path
#        self.arg_parser = arg_parser
#        self.options = self.arg_parser.parse_args()
#        self.log = create_logger(self.options.debug)

    def run(self):
        try:
            if self.options.profile:
                file = '%s.prof.%d' % (os.path.basename(self.script_path), os.getpid())
                cProfile = __import__('cProfile')
                pstats = __import__('pstats')
                cProfile.runctx("self.do_run()", globals(), locals(), file)
                p = pstats.Stats(file)
                p.strip_dirs()
                p.sort_stats('time', 'calls')
                p.print_stats()
                return 0 # TODO: return exit status
            else:
                return self.do_run()
        except KeyboardInterrupt:
            print
            print "Keyboard interrupt. exiting..."

    def do_run(self):
        raise Exception("This is a template method implemented by sub-class")

    def check_hosts(self):
        return check_hosts(self.options.__dict__, self.log, self.arg_parser.format_usage)

    def confirm_execution_on_production(self, message):
        if os.environ.get('TOMAHAWK_ENV') != 'production':
            return

        input = raw_input(message)
        if input == 'yes':
            print
        else:
            print "Command execution was cancelled."
            sys.exit(0)

    @classmethod
    def add_common_arguments(cls, parser):
        parser.add_argument(
            '-h', '--hosts', metavar='HOSTS',
            help='Host names for sending commands. (splited with ",")',
        )
        parser.add_argument(
            '-f', '--hosts-files', metavar='HOST_FILE',
            help='Hosts files which listed host names. (splited with ",")'
        )
        parser.add_argument(
            '-c', '--continue-on-error', action='store_true', default=None,
            help='Command exectuion continues whatever any errors.'
        )
        parser.add_argument(
            '-p', '--parallel', metavar='NUM', type=int, default=1,
            help='Process numbers for parallel command execution. (default: 1)'
        )
        parser.add_argument(
            '-l', '--prompt-login-password', action='store_true',
            help='Prompt a password for ssh authentication.'
        )
        parser.add_argument(
            '-t', '--timeout', metavar='SECONDS', type=int, default=DEFAULT_TIMEOUT,
            help='Specify expect timeout in seconds. (default: %d)' % (DEFAULT_TIMEOUT)
        )
        parser.add_argument(
            '--expect-timeout', metavar='SECONDS', type=int,
            help='Duplicated. Use --timeout'
        )
        parser.add_argument(
            '--expect-encoding', metavar='ENCODING', default=DEFAULT_EXPECT_ENCODING,
            help='Expect encoding for password prompt. (default: %s)' % (DEFAULT_EXPECT_ENCODING)
        )
        parser.add_argument(
            '-d', '--delay', type=int, default=0,
            help='Command delay time in seconds. (default: 0)'
        )
        parser.add_argument(
            '--expect-delay', type=float, default=DEFAULT_EXPECT_DELAY,
            help='Expect delay time in seconds. (default: 0.05)'
        )
        parser.add_argument(
            '-D', '--debug', action='store_true', default=False,
            help='Enable debug output.',
        )
        parser.add_argument(
            '--profile', action='store_true', help='Enable profiling.'
        )
        parser.add_argument(
            '--version', action='version', version='%(prog)s ' + VERSION
        )
        return parser

class BaseExecutor(object):
    """
    A base class for CommandExecutor, RsyncExecutor
    """
    def __init__(self, context, log, hosts=[], **kwargs):
        """
        Constructor
        
        Args:
        context -- context
        log -- log
        hosts -- target hosts
        """
        if context is None:
            raise RuntimeError('Argument "context" required.')
        if len(hosts) == 0:
            raise RuntimeError('Argument "hosts" length must be > 0')

        options = context.options
        if options['expect_timeout'] is not None:
            options['timeout'] = options['expect_timeout']
            log.warn("Option --expect-timeout is duplicated. Use --timeout.")

        newline = False
        login_password = None
        if 'login_password' in kwargs:
            login_password = kwargs['login_password']
        elif options.get('prompt_login_password'):
            login_password = read_login_password()
            newline = True
        
        sudo_password = None
        if 'sudo_password' in kwargs:
            sudo_password = kwargs['sudo_password']
        elif options.get('prompt_sudo_password') \
             or (not options.get('no_sudo_password') \
                 and context.arguments is not None
                 and context.arguments[0].startswith('sudo')):
            sudo_password = read_sudo_password()
            newline = True

        if newline:
            print

        self.context = context
        self.log = log
        self.hosts = hosts
        self.login_password = login_password
        self.sudo_password = sudo_password
        self.raise_error = False if options['continue_on_error'] else True
        self.process_pool = multiprocessing.Pool(processes = options['parallel'])
        
    def destory_process_pool(self):
        if self.process_pool is not None:
            self.process_pool.close()

    def __del__(self):
        self.destory_process_pool()
