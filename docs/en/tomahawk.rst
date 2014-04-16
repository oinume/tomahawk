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

ssh
^^^
tomahawk executes a command via 'ssh'. You can specify options for ssh with -o/--ssh-options and can configure ssh behavior with $HOME/.ssh/config.

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
tomahawk executes commands via shell(/bin/sh), so you can use '|' (pipe), '&&', '||' operators and so on. ::

  $ tomahawk -h host1,host2 'ps auxww | grep python'


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
Prompts a password for ssh authentication at first. If the password is all the same between target hosts, you'll input a password just once.

--login-password-stdin
^^^^^^^^^^^^^^^^^^^^^^
Read a SSH password from stdin instead of prompting.

-s, --prompt-sudo-password
^^^^^^^^^^^^^^^^^^^^^^^^^^
Prompts a password for sudo.

-c, --continue-on-error
^^^^^^^^^^^^^^^^^^^^^^^
Continues to send commands even if any errors.
The default behavior is fail-safe, means that tomahawk will stop if any errors.

-p, --parallel
^^^^^^^^^^^^^^
Specifies a number of processes for parallel command execution. (default: 1)
If your machine has multiple cpu cores, --parallel 2 .. N might be faster.

-t, --timeout
^^^^^^^^^^^^^
Specifies timeout seconds for a command.

-u, --ssh-user
^^^^^^^^^^^^^^
Specifies ssh user. The default is a current logged in user.

-o, --ssh-options
^^^^^^^^^^^^^^^^^
Specifies ssh options.

-F, --output-format
^^^^^^^^^^^^^^^^^^^
Specifies command output format.
The default is ``'${user}@${host} % ${command}\n${output}\n'``

-V, --verify-output
^^^^^^^^^^^^^^^^^^^
Verify command output of all hosts.
For additional information, see :ref:`checking-files-on-remote-hosts`

-C, --conf
^^^^^^^^^^
Specifies configuration file path. For additional information, see :ref:`omit-command-line-options`

ENVIRONMENT VARIABLES
---------------------
.. include:: _tomahawk_env_vars.rst


SEE ALSO
--------
* :manpage:`tomahawk-rsync(1)`
* :manpage:`ssh(1)`

