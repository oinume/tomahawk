# -*- coding: utf-8 -*-
from getpass import getpass, getuser
import sys

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

