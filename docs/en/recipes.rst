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

