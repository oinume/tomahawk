#!/usr/bin/env python
# -*- coding: utf-8 -*-
# A mock program of ssh command.

import argparse
import os
import re
import shlex
import subprocess
import sys

print("argv = " + str(sys.argv))

parser = argparse.ArgumentParser(
    prog = os.path.basename(__file__),
    description = 'A mock program of ssh command.',
    conflict_handler = 'resolve'
)
parser.add_argument(
    'command', metavar='command', nargs='+',
    help='Command executed on remote hosts.',
)
parser.add_argument(
    '-p', '--prompt', metavar='PROMPT_STRING',
    help='Prompt with given string.',
)
parser.add_argument(
    '-c', metavar='CIPHER_SPEC',
    help='Selects the cipher specification for encrypting the session.',
)
parser.add_argument(
    '-l', metavar='LOGIN_NAME',
    help='Specifies the user to log in as on the remote machine.',
)

options = parser.parse_args()
if options.prompt:
    print("before raw_input()")
    input = raw_input(options.prompt)
    #sys.stdin.read()
    print("input = " + input)

# call command
#regexp = re.compile("^/bin/sh -c '(.+)'$")
#for arg in options.command:
#    if regexp.match(arg):
#        exit(subprocess.call(shlex.split(arg)))
