#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import shlex
import subprocess

regexp = re.compile("^/bin/sh -c '(.+)'$")
for arg in sys.argv:
#    print arg
#    matches = regexp.search(arg)
    if regexp.match(arg):
        exit(subprocess.call(shlex.split(arg)))

