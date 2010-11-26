#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bootstrap import set_lib_path
set_lib_path(__file__)

from tomahawk.expect import CommandWithExpect

c = CommandWithExpect("/bin/bash -c 'sudo uptime'", '4qposs6nob', '4qposs6nob')
c.execute()
