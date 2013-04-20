tomahawk Recipes
================
Describes how to use tomahawk.

.. highlight:: bash

Formatting output
-----------------
-F (--output-format) option can change tomahawk's output. ::

  $ tomahawk -h <hosts> -F '[${host}] ${output}' -h <hosts> 'date'

  [localhost] Sat Jun  2 02:21:39 JST 2012
  [127.0.0.1] Sat Jun  2 02:21:40 JST 2012

You can speficy following variables.
* ${user}
* ${host}
* ${command}
* ${output}

Checking a file in remote hosts is all the same
-----------------------------------------------
At first, copy a file to be compared to remote hosts. ::

  $ tomahawk-rsync -h <hosts> /usr/local/apache2/conf/httpd.conf /tmp/httpd.conf

And then, diff 2 files with -V (--verify-output) option. ::

  $ tomahawk -h <hosts> -V 'diff /tmp/httpd.conf /usr/local/apache2/conf/httpd.conf 
  ...
  [error] Detected different command output on following hosts.
  ...

Omit command line options by --conf option
------------------------------------------
Since v0.6.0, you can omit command line options by a configuration file. If -c/--conf option is specified, tomahawk and tomahawk-rsync read command line options from a configuration file.

Configuration file is just ini file like below.::

  [tomahawk]
  options = --parallel 1
  
  [tomahawk-rsync]
  options = --parallel 1

That is equivalent to::

  $ tomahawk --parallel 1
  $ tomahawk-rsync --parallel 1

It is good to define commonly-used options in a configuration file.
