:orphan:

.. highlight:: bash

tomahawk-rsync manual page
==========================

SYNOPSIS
--------

**tomahawk-rsync** [*options*] source destination

DESCRIPTION
-----------

.. include:: _tomahawk-rsync_description.rst

rsync
^^^^^
tomahawk-rsync copies files via 'rsync'. You can specify options for rsync with -o/--rsync-ooptions.

OPTIONS
-------
These programs follow the usual GNU command line syntax, with long options starting with two dashes ('--').
A summary of options is included below.
For a complete description, see the Info files.

-H, --hosts
^^^^^^^^^^^
Specifies host names for sending commands. You can specify multiple hosts with ','.

-f, --hosts-files
^^^^^^^^^^^^^^^^^
Specifies hosts files which listed host names for sending commands.
You can specify multiple hosts files with ','.

Format of hosts file is below. ::

  web01
  web02
  #web03
  web04

A line of starting with '#' disables a host.

-l, --prompt-login-password
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Prompts a password for ssh authentication of rsync at first. If the password is all the same between target hosts, you'll input a password just once.

-c, --continue-on-error
^^^^^^^^^^^^^^^^^^^^^^^
Continues to send commands even if any errors.
The default behavior is fail-safe, means that tomahawk will stop if any errors.

-p, --parallel
^^^^^^^^^^^^^^
Specifies a number of processes for parallel command execution. (default: 1)
If your machine has many cpu cores, --parallel 2 .. N might be faster.

-t, --timeout
^^^^^^^^^^^^^
Specifies timeout seconds for a command.

-F, --output-format
^^^^^^^^^^^^^^^^^^^
Specifies command output format.
The default is '${user}@${host} % ${command}\n${output}\n'

-u, --rsync-user
^^^^^^^^^^^^^^^^
Specifies rsync user. The default is a current logged in user.

-o, --rsync-options
^^^^^^^^^^^^^^^^^^^
Specifies rsync options. The default is '-av'

-m, --mirror-mode
^^^^^^^^^^^^^^^^^
Selection of 'push' or 'pull'.
'pull' means copy files from remote to local. The default is 'push'.

-C, --conf
^^^^^^^^^^
Specifies configuration file path. For additional information, see :ref:`omit-command-line-options`


ENVIRONMENT VARIABLES
---------------------
.. include:: _tomahawk_env_vars.rst


SEE ALSO
--------
* :manpage:`tomahawk(1)`
* :manpage:`ssh(1)`
* :manpage:`rsync(1)`
