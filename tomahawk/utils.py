# -*- coding: utf-8 -*-
from six import print_
from six.moves import configparser

#import ConfigParser
from getpass import getpass, getuser
import os
import sys
import shlex

def shutdown_by_signal(signum, frame):
    print_()
    print_('Shutting down by signal %d.' % signum)
    # TODO: this function called twice
    sys.exit(signum)

def read_login_password():
    password = None
    while True:
        password = getpass("Enter a password for ssh authentication: ")
        if len(password) > 0:
            return password

def read_login_password_from_stdin():
    for line in sys.stdin:
        return line.rstrip()

def read_sudo_password():
    password = None
    while True:
        password = getpass("Enter a password for sudo: ")
        if len(password) > 0:
            return password

def read_sudo_password_from_stdin():
    for line in sys.stdin:
        return line.rstrip()

def get_run_user():
    return getuser()

def get_options_from_conf(command, conf_path):
    if not os.path.exists(conf_path):
        return []
    parser = configparser.ConfigParser()
    try:
        parser.read(conf_path)
        value = parser.get(command, 'options')
        if not value:
            return []
        return shlex.split(value.strip())
    except configparser.NoOptionError:
        e = sys.exc_info()[1]
        # ConfigParser.NoOptionError: No option 'options' in section: 'tomahawk'
        print_('[WARNING] %s. in "%s"' % (e, conf_path), file=sys.stderr)
        return []

def check_hosts(options, log, usage_func):
    if options.get('hosts') is not None and options.get('hosts_files') is not None:
        print_('Cannot specify both options --hosts and --hosts-files.', file=sys.stderr)
        print_(usage_func(), file=sys.stderr)
        sys.exit(1)

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
            except IOError:
                e = sys.exc_info()[1]
                print_('Failed to open "%s". (%s)' % (file, e), file=sys.stderr)
                sys.exit(4)
    else:
        print_('Specify -H/--hosts or -f/--hosts-files option.', file=sys.stderr)
        print_(usage_func(), file=sys.stderr)
        sys.exit(1)

    # Adjust parallel execution numbers with count of hosts
    parallel = options.get('parallel', 1)
    if len(hosts) < parallel:
        options['parallel'] = len(hosts)
    
    return hosts

def get_home_dir(file):
    abspath = os.path.abspath(file)
    parent, dir = None, None
    if abspath.find('internal') != -1 or abspath.find('external') != -1:
        parent, dir = os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(file))))
    else:
        parent, dir = os.path.split(os.path.dirname(os.path.abspath(file)))
    return parent

def check_required_command(command):
    def is_executable(path):
        return os.path.exists(path) and os.access(path, os.X_OK)

    dir, name = os.path.split(command)
    if dir and is_executable(command):
        return
    else:
        for dir in os.environ['PATH'].split(os.pathsep):
            exe = os.path.join(dir, command)
            if is_executable(exe):
                return
    print_('Program "%s" is not executable. Check installation.' % (command), file=sys.stderr)
    sys.exit(1)
