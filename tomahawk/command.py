# -*- coding: utf-8 -*-
import argparse
import getpass
import os
import signal
import string
import sys
import time

from tomahawk.base import BaseContext, BaseExecutor, BaseMain
from tomahawk.constants import (
    TimeoutError,
    DEFAULT_COMMAND_OUTPUT_FORMAT
)
from tomahawk.expect import CommandWithExpect
from tomahawk.utils import shutdown_by_signal

class CommandContext(BaseContext):
    """
    Command context
    """
    def __init__(self, arguments, options, out, err):
        super(CommandContext, self).__init__(options, out, err)
        self.arguments = arguments

class CommandMain(BaseMain):
    """
    Main class for tomahawk
    """

    def __init__(self, file):
        # setup self.log, self.arg_parser, self.options
        super(CommandMain, self).__init__(file)
        self.log.debug("options = " + str(self.options))
        self.log.debug("arguments = " + str(self.options.command))

    def do_run(self):
        context = CommandContext(
            self.options.command,
            self.options.__dict__,
            sys.stdout,
            sys.stderr
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
        parser.add_argument(
            '--output-format', default=DEFAULT_COMMAND_OUTPUT_FORMAT,
            help="Command output format. (default: '%s')" % (DEFAULT_COMMAND_OUTPUT_FORMAT.replace('%', '%%').replace('\n', '\\n'))
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

        #######################
        # callbacks
        #######################
        def create_output(color, output_format_template, command, host, exit_status, command_output):
            c = command
            if exit_status == 0:
                c = color.green(command)
            return output_format_template.safe_substitute({
                'user': ssh_user,
                'host': host,
                'command': c,
                'output': command_output,
            })

        def create_timeout_message(color, output, timeout):
            output += 'Command timed out after %d seconds' % (options['timeout'])
            return output

        def create_timeout_raise_error_message(color, command, host, timeout):
            return 'Command "%s" timed out on host "%s" after %d seconds' \
                % (command, host, timeout)

        def create_failure_message(color, output, exit_status):
            output += 'Command failed ! (status = %d)' % exit_status
            return output

        def create_failure_raise_error_message(color, command, host):
            return 'Command "%s" failed on host "%s"' % (command, host)

        def create_failure_last_message(color, command, hosts):
            return 'Command "%s" failed on following hosts\n%s' % (command, hosts)

        # Call BaseExectuor#process_async_results with callbacks
        return self.process_async_results(
            async_results,
            create_output,
            create_timeout_message,
            create_timeout_raise_error_message,
            create_failure_message,
            create_failure_raise_error_message,
            create_failure_last_message
        )
