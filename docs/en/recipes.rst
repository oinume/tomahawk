tomahawk Recipes
================
Describes how to use tomahawk.

.. highlight:: bash

Formatting output
-----------------
``-F/--output-format`` option can change tomahawk's output. ::

  $ tomahawk -h <hosts> -F '[${host}] ${output}' -h <hosts> 'date'

  [localhost] Sat Jun  2 02:21:39 JST 2012
  [127.0.0.1] Sat Jun  2 02:21:40 JST 2012

You can speficy following variables.

* ${user}
* ${host}
* ${command}
* ${output}

.. _checking-files-on-remote-hosts:

Checking files on remote hosts
------------------------------
Since v0.6.0, able to check files on remote hosts are all the same.
Let's check httpd.conf is all the same with ``md5sum`` command. ::

  $ tomahawk -h <hosts> -V 'md5sum /usr/local/apache2/conf/httpd.conf'

If output of some hosts are different, you'll get following errors. ::

  ...
  [error] Detected different command output on following hosts.
  ...

.. _omit-command-line-options:

Omit command line options by a configuration file.
--------------------------------------------------
Since v0.6.0, you can omit command line options by a configuration file. If ``-c/--conf`` option is specified, tomahawk and tomahawk-rsync read command line options from a configuration file. It is good to define commonly-used options in a configuration file.

Configuration file is just ini file like below. ::

  [tomahawk]
  options = --parallel 1
  
  [tomahawk-rsync]
  options = --parallel 1

That is equivalent to ::

  $ tomahawk --parallel 1
  $ tomahawk-rsync --parallel 1

