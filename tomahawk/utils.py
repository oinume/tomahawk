# -*- coding: utf-8 -*-
from getpass import getpass, getuser
import sys
import os

def shutdown_by_signal(signum, frame):
    print
    print 'Shutting down by signal %d.' % signum;
    # TODO: this function called twice
    sys.exit(signum);

def read_login_password():
    password = None
    while True:
        password = getpass('Enter a password for ssh authentication: ')
        if len(password) > 0:
            return password

def read_sudo_password():
    password = None
    while True:
        password = getpass('Enter a password for sudo: ')
        if len(password) > 0:
            return password

def get_run_user():
    return getuser()

def check_hosts(options, log, usage_func):
    if options.get('hosts') is not None and options.get('hosts_files') is not None:
        log.error("Cannot specify both options --hosts and --hosts-files.")
        log.error(usage_func())
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
        log.error("Specify --hosts or --hosts-files option.")
        log.error(usage_func())
        sys.exit(2)

    return hosts

def get_home_dir(file):
    abspath = os.path.abspath(file)
    parent, dir = None, None
    if abspath.find('internal') != -1 or abspath.find('external') != -1:
        parent, dir = os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(file))))
    else:
        parent, dir = os.path.split(os.path.dirname(os.path.abspath(file)))
    return parent

