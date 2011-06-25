# -*- coding: utf-8 -*-
import argparse
import getpass
import os
import signal
import sys
import time

from tomahawk.base import BaseContext, BaseExecutor, BaseMain
from tomahawk.constants import TimeoutError
from tomahawk.expect import CommandWithExpect
from tomahawk.utils import shutdown_by_signal

class CommandContext(BaseContext):
    """
    Command context
    """
    def __init__(self, arguments, options):
        self.arguments = arguments
        self.options = options

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

def _command(
    command, command_args, login_password, sudo_password,
    timeout, expect_delay, debug_enabled):
    """
    Execute a command.
    """
    # Trap SIGINT(Ctrl-C) to quit executing a command
    signal.signal(signal.SIGINT, shutdown_by_signal)

    return CommandWithExpect(
        command, command_args, login_password,
        sudo_password, timeout, expect_delay, debug_enabled
    ).execute()

class CommandExecutor(BaseExecutor):
    """
    Execute commands.

    Args:
    commands -- commands to execute.
    
    Returns: when rsync succeeds, return 0. When errors, return 1
    """
    def execute(self, commands):
        if len(commands) == 0:
            raise RuntimeError('1st argument "commands" length is 0')

        options = self.context.options
        #ssh = options.get('ssh') or 'ssh'
        
        ssh_user = options.get('ssh_user') or getpass.getuser()
        ssh_options = ''
        if options.get('ssh_options'):
            ssh_options = options['ssh_options'] + ' '
        ssh_options += '-l ' + ssh_user

        async_results = []
        for host in self.hosts:
            for command in commands:
                command_args = []
                for option in ssh_options.split(' '):
                    #  remove left and right whitespaces
                    command_args.append(option.strip())

                command_args.append(host)
                c = command.replace('"', '\\"')
                # execute a command with shell because we want to use pipe(|) and so on.
                command_args.extend([ '/bin/sh', '-c', '"%s"' % (c) ])

                # host, command, ssh_user, ssh_option, login_password, sudo_password
                async_result = self.process_pool.apply_async(
                    _command,
                    ( 'ssh', command_args, self.login_password,
                      self.sudo_password, options['timeout'],
                      options['expect_delay'], options['debug'] ),
                )
                async_results.append({ 'host': host, 'command': command, 'async_result': async_result })

                if options['delay'] != 0:
                    time.sleep(options['delay'])

        hosts_count = len(self.hosts)
        finished = 0
        error_hosts = {}
        while finished < hosts_count:
            for dict in async_results:
                host = dict['host']
                async_result = dict['async_result']
                if not async_result.ready():
                    continue

                exit_status = 1
                command_output = ''
                timeout_detail = None
                try:
                    exit_status, command_output = async_result.get(timeout = options['timeout'] + 1)
                except TimeoutError, error:
                    timeout_detail = str(error)
                async_results.remove(dict)
                finished += 1

                output_params = {
                    'user': ssh_user,
                    'host': host,
                    'command': dict['command'],
                    'output': command_output,
                }
                # output template
                # TODO: specify from command line option
                output = '%(user)s@%(host)s %% %(command)s\n%(output)s' % output_params
                if exit_status == 0:
                    print output, '\n'
                elif timeout_detail is not None:
                    output += '[error] Command timed out after %d seconds' % (options['timeout'])
                    print output, '\n'
                    error_hosts[host] = 2
                    if self.raise_error:
                        print >> sys.stderr, '[error] Command "%s" timed out on host "%s" after %d seconds' % (command, host, options['timeout'])
                        return 1
                else:
                    output += '[error] Command failed ! (status = %d)' % exit_status
                    print output, '\n'
                    error_hosts[host] = 1
                    if self.raise_error:
                        #raise RuntimeError("[error] Command '%s' failed on host '%s'" % (command, host))
                        print >> sys.stderr, '[error] Command "%s" failed on host "%s"' % (command, host)
                        return 1

        if len(error_hosts) != 0:
            hosts = ''
            for h in self.hosts:
                if h in error_hosts:
                    hosts += '  %s\n' % (h)
            hosts = hosts.rstrip()
            print >> sys.stderr, '[error] Command "%s" failed on following hosts\n%s' % (command, hosts)
            return 1
        
        return 0
