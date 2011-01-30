#!/usr/bin/env python
# -*- coding: utf-8 -*-
# A mock program of ssh command.

import argparse
import os
import re
import shlex
import subprocess

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

options = parser.parse_args()
if options.prompt:
    input = raw_input(options.prompt)
else:
    regexp = re.compile("^/bin/sh -c '(.+)'$")
    for arg in options.command:
        if regexp.match(arg):
            exit(subprocess.call(shlex.split(arg)))
