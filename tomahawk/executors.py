# -*- coding: utf-8 -*-
from getpass import getuser
import multiprocessing
from os import path
import signal
import sys
from time import sleep
from tomahawk.constants import DEFAULT_RSYNC_OPTIONS, TimeoutError
from tomahawk.expect import CommandWithExpect
from tomahawk.utils import read_login_password, read_sudo_password, shutdown_by_signal

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
        
        ssh_user = options.get('ssh_user') or getuser()
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
                    sleep(options['delay'])

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
        rsync_user = options.get('rsync_user') or getuser()
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
                if path.exists(destination):
                    if path.isdir(destination):
                        # if destination is a directory, gets a source filename and appends a host suffix
                        file_name = path.basename(source)
                        if not destination.endswith('/'):
                            dest += '/'
                        dest += '%s__%s' % (host, file_name)
                    else:
                        # if destination is a file, simply appends a host suffix
                        dest = host + '__' + dest
                else:
                     # if file doesn't exist
                    source_name = path.basename(source[0:len(source)-1]) if source.endswith('/') else path.basename(source)
                    dest += host + '__' + source_name
                c = rsync_template % (host, dest)
            
            self.log.debug('command = "%s"' % (c))

            async_result = self.process_pool.apply_async(
                _rsync,
                ( c, self.login_password, options['timeout'], options['expect_delay'], options['debug'] )
            )
            async_results.append({ 'host': host, 'command': c, 'async_result': async_result })

            if options['delay'] != 0:
                sleep(options['delay'])

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
