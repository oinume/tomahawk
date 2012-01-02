:orphan:

.. highlight:: bash

tomahawk-rsync manual page
==========================

SYNOPSIS
--------

**tomahawk-rsync** [*options*] source destination

DESCRIPTION
-----------

:program:`tomahawk-rsync` is a program that enables to copy files <into/from> many hosts. ::

  $ tomahawk-rsync -h host1,host2,host3 test.py /tmp/test.py

---> "test.py" is copied to host1, host2 and host3. ::

  $ tomahawk-rsync -f web.list /usr/local/apache2/conf/httpd.conf /tmp/httpd.conf

---> "httpd.conf" is copied to hosts which listed in "web.list". ::

  $ tomahawk-rsync -h host1,host2 -m pull /usr/local/apache2/conf/httpd.conf /tmp/conf/

---> "httpd.conf" is copied from host1 and host2 to local directory /tmp/conf as "host1__httpd.conf" and "host2__httpd.conf".


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

Prompts a password for ssh authentication at first. If the password is all the same between target hosts, you'll input a password just once.

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

--output-format
^^^^^^^^^^^^^^^

Specifies command output format.
The default is '${user}@${host} % ${command}\n${output}\n'

-u, --rsync-user
^^^^^^^^^^^^^^^^

Specifies rsync user. The default is a current logged in user.

-o, --rsync-options
^^^^^^^^^^^^^^^^^^^

Specifies rsync options. The default is '-avz'

-m, --mirror-mode
^^^^^^^^^^^^^^^^^

Selection of "push" or "pull".
"pull" means copy files from remote to local (default: "push")


SEE ALSO
--------

* :manpage:`tomahawk(1)`
* :manpage:`ssh(1)`
* :manpage:`rsync(1)`
