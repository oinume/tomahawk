# -*- coding: utf-8 -*-
import multiprocessing
import os
import re
import platform
from six import print_
import six
import string
import sys

from tomahawk import (
    __version__,
    TimeoutError,
)
from tomahawk.color import (
    create_coloring_object
)
from tomahawk.constants import (
    DEFAULT_TIMEOUT,
    DEFAULT_COMMAND_OUTPUT_FORMAT,
    DEFAULT_EXPECT_DELAY,
    DEFAULT_EXPECT_ENCODING,
    OUTPUT_FORMAT_CONTROLL_CHARS,
)
from tomahawk.log import create_logger
from tomahawk.utils import (
    check_hosts,
    get_options_from_conf,
    read_login_password,
    read_login_password_from_stdin,
    read_sudo_password,
    read_sudo_password_from_stdin
)
class BaseContext(object):
    def __init__(self, options = {}, out = sys.stdout, err = sys.stderr):
        self.options = options
        self.out = out
        self.err = err
        self.arguments, self.source, self.destination = None, None, None

class BaseMain(object):
    def __init__(self, script_path):
        self.script_path = script_path
        self.arg_parser = self.create_argument_parser(script_path)
        self.options = self.arg_parser.parse_args(sys.argv[1:])
        conf_options = None
        if self.options.conf:
            conf_options = get_options_from_conf(
                os.path.basename(script_path),
                self.options.conf
            )
            args = conf_options + sys.argv[1:]
            # Re-parse command line options because conf_options added
            self.options = self.arg_parser.parse_args(args)

        self.log = create_logger(
            None,
            self.options.debug or self.options.deep_debug,
            self.options.deep_debug
        )
        if conf_options:
            self.log.debug("Applying options %s from %s" % (str(conf_options), self.options.conf))

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
            print_()
            print_('Keyboard interrupt. exiting...')

    def do_run(self):
        raise Exception("This is a template method implemented by sub-class")

    def check_hosts(self):
        return check_hosts(self.options.__dict__, self.log, self.arg_parser.format_usage)

    def confirm_execution_on_production(self, message):
        if os.environ.get('TOMAHAWK_ENV') != 'production':
            return

        input = raw_input(message)
        if input == 'yes':
            print_()
        else:
            print_('Command execution was cancelled.')
            sys.exit(0)

    @classmethod
    def add_common_arguments(cls, parser):
        parser.add_argument(
            '-h', '--hosts', metavar='HOSTS',
            help='DUPLICATED. Use -H. (Will be deleted in v0.8.0)',
        )
        parser.add_argument(
            '-H', '--hosts', metavar='HOSTS',
            help='Host names for sending commands. (splited with ",")',
        )
        parser.add_argument(
            '-f', '--hosts-files', metavar='HOSTS_FILES',
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
            '--login-password-stdin', action='store_true',
            help='Read a password for ssh authentication from stdin.'
        )
        parser.add_argument(
            '-t', '--timeout', metavar='SECONDS', type=int, default=DEFAULT_TIMEOUT,
            help='Specify expect timeout in seconds. (default: %d)' % (DEFAULT_TIMEOUT)
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
            '-C', '--conf', metavar='FILE', default=None,
            help='Configuration file path.'
        )
        parser.add_argument(
            '-D', '--debug', action='store_true', default=False,
            help='Enable debug output.',
        )
        parser.add_argument(
            '--deep-debug', action='store_true', default=False,
            help='Enable deeper debug output.',
        )
        parser.add_argument(
            '--profile', action='store_true', help='Enable profiling.'
        )
        parser.add_argument(
            '--version', action='version',
            version='%(prog)s ' + __version__
            + ' with Python ' + '.'.join(map(str, sys.version_info[0:3]))
            + ' (' + platform.platform() + ')'
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
        self.processes_terminated = False
        if context is None:
            raise RuntimeError('Argument "context" required.')
        if len(hosts) == 0:
            raise RuntimeError('Argument "hosts" length must be > 0')

        options = context.options
        newline = False
        login_password = None
        if 'login_password' in kwargs:
            login_password = kwargs['login_password']
        elif options.get('prompt_login_password'):
            login_password = read_login_password()
            newline = True
        elif options.get('login_password_stdin'):
            login_password = read_login_password_from_stdin()

        sudo_password = None
        if 'sudo_password' in kwargs:
            sudo_password = kwargs['sudo_password']
        elif options.get('prompt_sudo_password'):
            sudo_password = read_sudo_password()
        elif options.get('sudo_password_stdin'):
            sudo_password = read_sudo_password_from_stdin()

        if newline:
            print_()

        self.context = context
        self.log = log
        self.hosts = hosts
        self.login_password = login_password
        self.sudo_password = sudo_password
        self.raise_error = True
        if options.get('continue_on_error'):
            self.raise_error = False
        self.process_pool = multiprocessing.Pool(processes = options.get('parallel', 1))

    def process_async_results(
        self,
        async_results,
        create_output,
        create_timeout_message,
        create_timeout_raise_error_message,
        create_failure_message,
        create_failure_raise_error_message,
        create_failure_last_message,
    ):
        out, err = self.context.out, self.context.err
        color = create_coloring_object(out)
        options = self.context.options
        hosts_count = len(self.hosts)
        finished = 0
        error_hosts_count = 0
        output_format = self.output_format(options.get('output_format', DEFAULT_COMMAND_OUTPUT_FORMAT))
        if six.PY2:
            output_format = output_format.decode(DEFAULT_EXPECT_ENCODING)
        output_format_template = string.Template(output_format)
        timeout = options.get('timeout', DEFAULT_TIMEOUT)
        error_prefix = color.red(color.bold('[error]')) # insert newline for error messages

        execution_info = {}
        # Main loop continues until all processes are done
        while finished < hosts_count:
            for dict in async_results:
                host = dict['host']
                command = dict['command']
                async_result = dict['async_result']
                if not async_result.ready():
                    continue

                exit_status = 1
                command_output = ''
                timeout_detail = None
                try:
                    exit_status, command_output = async_result.get(timeout = timeout)
                    self.log.debug("host = %s, exit_status = %d" % (host, exit_status))
                except (TimeoutError, multiprocessing.TimeoutError):
                    error = sys.exc_info()[1]
                    timeout_detail = str(error)
                    execution_info[host] = { 'timeout': 1 }
                async_results.remove(dict)
                finished += 1

                output = create_output(color, output_format_template, command, host, exit_status, command_output)
                execution_info[host] = {
                    'exit_status': exit_status,
                    'command_output': command_output,
                    'timeout': False,
                }
                if command_output == '':
                    # if command_output is empty, chomp last newline character for ugly output
                    output = re.sub(os.linesep + r'\Z', '', output)

                if exit_status == 0:
                    if six.PY2:
                        output = output.encode(DEFAULT_EXPECT_ENCODING)
                    print_(output, file=out)
                elif timeout_detail is not None:
                    print_('%s %s\n' % (
                        error_prefix,
                        create_timeout_message(color, output, timeout)
                    ), file=out)
                    execution_info[host]['timeout'] = True
                    error_hosts_count += 1
                    if self.raise_error:
                        print_('%s %s\n' % (
                            error_prefix,
                            create_timeout_raise_error_message(color, command, host, timeout)
                        ), file=err)
                        return 1
                else:
                    print_('%s %s\n' % (
                        error_prefix,
                        create_failure_message(color, output, exit_status)
                    ), file=out)
                    error_hosts_count += 1
                    if self.raise_error:
                        print_('%s %s' % (
                            error_prefix,
                            create_failure_raise_error_message(color, command, host)
                        ), file=err)
                        return 1

        # Free process pool
        self.terminate_processes()

        if error_hosts_count > 0:
            hosts = ''
            for h in self.hosts:
                if execution_info[h]['exit_status'] != 0:
                    hosts += '  %s\n' % (h)
            hosts = hosts.rstrip()
            print_('%s %s' % (
                error_prefix,
                create_failure_last_message(color, command, hosts)
            ), file=err)
            return 1

        if options.get('verify_output'):
            has_different_output = False
            prev_output = None
            hosts = ''
            for h in self.hosts:
                output = execution_info[h]['command_output']
                self.log.debug("host: '%s', prev_output: '%s', output = '%s'" % (h, prev_output, output))
                if prev_output != None and output != prev_output:
                    hosts += '  %s\n' % (h)
                    has_different_output = True
                prev_output = output
            hosts = hosts.rstrip()

            if has_different_output:
                print_("%s Detected different command output on following hosts.\n%s" \
                    % (color.red(error_prefix), hosts), file=err)
                return 3
            else:
                print_(color.green('Verified output of all hosts.'), file=out)

        return 0

    def output_format(self, format):
        seq = []
        prev, prev_prev = None, None
        for char in format:
            controll_char = OUTPUT_FORMAT_CONTROLL_CHARS.get(char)
            if controll_char and prev == '\\' and prev_prev == '\\':
                pass
            elif controll_char and prev == '\\':
                seq.pop(len(seq) - 1)
                seq.append(controll_char)
                prev_prev = prev
                prev = char
                continue

            seq.append(char)
            prev_prev = prev
            prev = char

        return ''.join(seq)

    def terminate_processes(self):
        if hasattr(self, 'process_pool') and not self.processes_terminated:
            #self.process_pool.close()
            self.log.debug("terminating processes")
            self.process_pool.terminate()
            self.process_pool.join()
            self.processes_terminated = True

    def __del__(self):
        self.terminate_processes()
