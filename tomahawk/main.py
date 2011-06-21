# -*- coding: utf-8 -*-
#from tomahawk.command_line import BaseMain
import argparse
import os
import sys

from tomahawk.command_line import CommandContext, RsyncContext
from tomahawk.constants import (
    VERSION,
    DEFAULT_TIMEOUT,
    DEFAULT_EXPECT_DELAY,
    DEFAULT_EXPECT_ENCODING,
    DEFAULT_RSYNC_OPTIONS
)
from tomahawk.executors import CommandExecutor, RsyncExecutor
from tomahawk.log import create_logger

class BaseMain(object):
    def __init__(self, file, bin_dir):
        pass
    
    def initialize(self, script_path, arg_parser):
        self.script_path = script_path
        self.arg_parser = arg_parser
        self.options = self.arg_parser.parse_args()
        self.log = create_logger(self.options.debug)

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
        options = self.options.__dict__
        if options.get('hosts') is not None and options.get('hosts_files') is not None:
            self.log.error("Cannot specify both options --hosts and --hosts-files.")
            self.log.error(self.arg_parser.format_usage())
            sys.exit(2)

        # initialize target hosts with --hosts or --hosts-files
        hosts = []
        # TODO: \, escape handling
        # regexp: [^\\],
        if options.get('hosts'):
            list = options['hosts'].split(',')
            for host in list:
                host.strip()
                hosts.append(host)
        elif options.get('hosts_files'):
            list = options['hosts_files'].split(',')
            for file in list:
                try:
                    for line in open(file):
                        host = line.strip()
                        if host == '' or host.startswith('#'):
                            continue
                        hosts.append(host)
                except IOError, e:
                    print >> sys.stderr, "Failed to open '%s'. (%s)" % (file, e)
                    sys.exit(4)
        else:
            self.log.error("Specify --hosts or --hosts-files option.")
            self.log.error(self.arg_parser.format_usage())
            sys.exit(2)

        return hosts

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

class CommandMain(BaseMain):
    """
    Main class for tomahawk
    """

    def __init__(self, file, bin_dir):
        # setup self.log, self.arg_parser, self.options
        super(CommandMain, self).initialize(file, self.create_argument_parser(file))
        self.log.debug("options = " + str(self.options))
        self.log.debug("arguments = " + str(self.options.command))

    def do_run(self):
        context = CommandContext(
            self.options.command,
            self.options.__dict__,
        )
        hosts = self.check_hosts()

        # prompt when production environment
        self.confirm_execution_on_production(
            'Command "%s" will be executed to %d hosts. Are you sure? [yes/NO]: '
            % (' '.join(context.arguments), len(hosts))
        )

        executor = CommandExecutor(context, self.log, hosts)
        return executor.execute(context.arguments)

    @classmethod
    def create_argument_parser(cls, file):
        parser = argparse.ArgumentParser(
            prog = os.path.basename(file),
            description = "A simple command executor for many hosts.",
            conflict_handler = 'resolve'
        )
        parser.add_argument(
            'command', metavar='command', nargs='+',
            help='Command executed on remote hosts.',
        )
        parser.add_argument(
            '--ssh', default='ssh', help='ssh program. (default: "ssh")'
        )
        parser.add_argument(
            '-u', '--ssh-user', help='ssh user.'
        )
        parser.add_argument(
            '-o', '--ssh-options', help='ssh options.'
        )
        parser.add_argument(
            '-s', '--prompt-sudo-password', action='store_true',
            help='Prompt a password for sudo.'
        )
        parser.add_argument(
            '--no-sudo-password', action='store_true',
            help='Never prompt a password for sudo.'
        )
        cls.add_common_arguments(parser)
        return parser

class RsyncMain(BaseMain):
    """
    Main class for tomahawk-rsync
    """

    def __init__(self, file, bin_dir):
        # setup self.log, self.arg_parser, self.options
        super(RsyncMain, self).initialize(file, self.create_argument_parser(file))
        self.log.debug("options = " + str(self.options))
        self.log.debug("source = " + str(self.options.source))
        self.log.debug("destination = " + str(self.options.destination))

    def do_run(self):
        context = RsyncContext(
            self.options.source,
            self.options.destination,
            self.options.__dict__,
        )
        hosts = self.check_hosts()

        # prompt when production environment
        rsync_command = 'rsync %s %s %s' % (context.options['rsync_options'], context.source, context.destination)
        self.confirm_execution_on_production(
            'Rsync command "%s" will be executed %d hosts. Are you sure? [yes/NO]: '
            % (rsync_command, len(hosts))
        )

        executor = RsyncExecutor(context, self.log, hosts)
        return executor.execute(context.source, context.destination)

    @classmethod
    def create_argument_parser(cls, file):
        parser = argparse.ArgumentParser(
            prog = os.path.basename(file),
            description = "A simple rsync executor for many hosts.",
            conflict_handler = 'resolve'
        )
        parser.add_argument(
            'source', metavar='source', help='source',
        )
        parser.add_argument(
            'destination', metavar='destination', help='destination',
        )
        parser.add_argument(
            '-u', '--rsync-user', help='rsync user.'
        )
        parser.add_argument(
            '-o', '--rsync-options', default=DEFAULT_RSYNC_OPTIONS,
            help='rsync options. (default: "-avz")'
        )
        parser.add_argument(
            '-m', '--mirror-mode',
            help='"push" or "pull". "pull" means copy files remote -> local (default: "push")'
        )
#       parser.add_argument(
#           '-a', '--append-host-suffix', action='store_true', default=True,
#           help='Append host name to destination file/dir (only when "--mirror-mode=pull").'
#       )
        cls.add_common_arguments(parser)
        return parser
