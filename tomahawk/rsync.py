# -*- coding: utf-8 -*-
import argparse
import getpass
import multiprocessing
import os
import signal
import sys
import time

from tomahawk.base import BaseContext, BaseMain, BaseExecutor
from tomahawk.constants import (
    DEFAULT_RSYNC_OPTIONS,
    TimeoutError,
)
from tomahawk.expect import CommandWithExpect
from tomahawk.utils import shutdown_by_signal

class RsyncContext(BaseContext):
    """
    """
    def __init__(self, source, destination, options, out, err):
        self.source = source
        self.destination = destination
        super(RsyncContext, self).__init__(options, out, err)

class RsyncMain(BaseMain):
    """
    Main class for tomahawk-rsync
    """

    def __init__(self, file):
        #arg_parser = self.create_argument_parser(file)
        # setup self.log, self.arg_parser, self.options
        super(RsyncMain, self).__init__(file)
        self.log.debug("options = " + str(self.options))
        self.log.debug("source = " + str(self.options.source))
        self.log.debug("destination = " + str(self.options.destination))

    def do_run(self):
        context = RsyncContext(
            self.options.source,
            self.options.destination,
            self.options.__dict__,
            sys.stdout,
            sys.stderr
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


def _rsync(command, login_password, timeout, expect_delay, debug_enabled):
    """
    Execute rsync
    """
    # Trap SIGINT(Ctrl-C) to quit executing a command
    signal.signal(signal.SIGINT, shutdown_by_signal)

    return CommandWithExpect(
        command, [], login_password,
        None, timeout, expect_delay, debug_enabled
    ).execute()

class RsyncExecutor(BaseExecutor):
    """
    Execute rsync.
    
    Args:
    source -- source file/dir
    destination -- destination file/dir
    
    Returns: when rsync succeeds, return 0. When errors, return 1
    """
    def execute(self, source, destination):
        if source is None:
            raise RuntimeError('1st argument "source" must not be None')
        if destination is None:
            raise RuntimeError('2nd argument "destination" must not be None')

        options = self.context.options
        rsync_user = options.get('rsync_user') or getpass.getuser()
        rsync_options = options.get('rsync_options') or DEFAULT_RSYNC_OPTIONS
        mirror_mode = options.get('mirror_mode') or 'push'
        if mirror_mode not in ('push', 'pull'):
            raise RuntimeError('Invalid mirror_mode: ' + mirror_mode)

        rsync_template = ''
        if mirror_mode == 'push':
            rsync_template = 'rsync %s %s %s@%%s:%s' % (
                rsync_options,
                source,
                rsync_user,
                destination,
            )
        else:
            rsync_template = 'rsync %s %s@%%s:%s %%s' % (
                rsync_options,
                rsync_user,
                source,
            )

        async_results = []
        error_hosts = {}
        for host in self.hosts:
            c = None
            if mirror_mode == 'push':
                c = rsync_template % (host)
            else: # pull
                dest = destination
                if os.path.exists(destination):
                    if os.path.isdir(destination):
                        # if destination is a directory, gets a source filename and appends a host suffix
                        file_name = os.path.basename(source)
                        if not destination.endswith('/'):
                            dest += '/'
                        dest += '%s__%s' % (host, file_name)
                    else:
                        # if destination is a file, simply appends a host suffix
                        dest = host + '__' + dest
                else:
                     # if file doesn't exist
                    source_name = os.path.basename(source[0:len(source)-1]) if source.endswith('/') else os.path.basename(source)
                    dest += host + '__' + source_name
                c = rsync_template % (host, dest)
            
            self.log.debug('command = "%s"' % (c))

            async_result = self.process_pool.apply_async(
                _rsync,
                ( c, self.login_password, options['timeout'], options['expect_delay'], options['debug'] )
            )
            async_results.append({ 'host': host, 'command': c, 'async_result': async_result })

            if options['delay'] != 0:
                time.sleep(options['delay'])

        finished = 0
        hosts_count = len(self.hosts)
        while finished < hosts_count:
            for dict in async_results:
                host = dict['host']
                async_result = dict['async_result']

                exit_status = 1
                command_output = ''
                timeout_detail = None
                try:
                    exit_status, command_output = async_result.get(timeout = options['timeout'])
                except (TimeoutError, multiprocessing.TimeoutError), error:
                    timeout_detail = str(error)
                async_results.remove(dict)
                finished += 1

                output = '%% %s\n%s' % (dict['command'], command_output)
                if exit_status == 0:
                    print output, '\n'
                elif timeout_detail is not None:
                    output += '[error] rsync timed out after %d seconds' % (options['timeout'])
                    print output, '\n'
                    error_hosts[host] = 2
                    if self.raise_error:
                        #raise RuntimeError("[error] '%s' failed on host '%s'" % (command, host))
                        print >> sys.stderr, '[error] "%s" timed out on host "%s" after %d seconds.' % (c, host, options['timeout'])
                        return 1
                else:
                    output += '[error] rsync failed ! (status = %d)' % exit_status
                    print output, '\n'
                    error_hosts[host] = 1
                    if self.raise_error:
                        #raise RuntimeError("[error] '%s' failed on host '%s'" % (command, host))
                        # TODO: failure_handler, timeout_handler
                        print >> sys.stderr, '[error] "%s" failed on host "%s"' % (c, host)
                        return 1

        if len(error_hosts) != 0:
            hosts = ''
            for h in self.hosts:
                if h in error_hosts:
                    hosts += '  %s\n' % (h)
            hosts.rstrip()

            rsync = None
            if mirror_mode == 'push':
                rsync = rsync_template % ('REMOTE_HOST')
            else:
                rsync = rsync_template % ('REMOTE_HOST', 'LOCAL')
            print >> sys.stderr, '[error] "%s" failed on following hosts\n%s' % (rsync, hosts)
            return 1

        return 0
