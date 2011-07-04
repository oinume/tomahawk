#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

print("This script is not executable.")
sys.exit(0)

# version input
# Changes
# tomahawk/constants.py VERSION = '0.2.2'
# upload

from tomahawk.constants import VERSION

new_version = raw_input("Release version [%s]: " % (VERSION))

#tomahawk.
