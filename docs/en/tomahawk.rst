:orphan:

.. highlight:: bash

tomahawk manual page
====================

SYNOPSIS
--------

**tomahawk** [*options*] command

DESCRIPTION
-----------

.. include:: _tomahawk_description.rst

hosts file
^^^^^^^^^^
-h option enables you to specify hosts, another option '-f', which is specifying hosts files.
hosts file is listing host names like this ::

  host1
  host2
  host3
  #host4

Starting with "#" means commenting the host out. 

shell operators
^^^^^^^^^^^^^^^
tomahawk executes commands via shell(/bin/sh), so you can use "|" (pipe), &&, || operators and so on. ::

  $ tomahawk -h host1,host2 'ps auxww | grep python'


OPTIONS
-------
These programs follow the usual GNU command line syntax, with long options starting with two dashes ('--').
A summary of options is included below.
For a complete description, see the Info files.

-h, --hosts
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
DUPLICATED. Use -P/--prompt-password. Will be deleted in v0.6.0

-P, --prompt-password
^^^^^^^^^^^^^^^^^^^^^
Prompts a password for ssh authentication at first. If the password is all the same between target hosts, you'll input a password just once.

--password-from-stdin
^^^^^^^^^^^^^^^^^^^^^
Read a password from stdin instead of prompting.

-s, --prompt-sudo-password
^^^^^^^^^^^^^^^^^^^^^^^^^^
OBSOLETED. Will be deleted in v0.6.0

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

--expect-timeout
^^^^^^^^^^^^^^^^
Duplicated. Use t (-timeout) instead.

-u, --ssh-user
^^^^^^^^^^^^^^
Specifies ssh user. The default is a current logged in user.

-o, --ssh-options
^^^^^^^^^^^^^^^^^
Specifies ssh options.

--output-format
^^^^^^^^^^^^^^^
Specifies command output format.
The default is '${user}@${host} % ${command}\n${output}\n'


SEE ALSO
--------
* :manpage:`tomahawk-rsync(1)`
* :manpage:`ssh(1)`
* :manpage:`scp(1)`
