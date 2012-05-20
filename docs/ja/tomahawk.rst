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
-h オプションでホストを指定する。-f オプションではホストが記載されたファイルのパスを指定する。
ホストのファイルは以下のような形式である。 ::

  host1
  host2
  host3
  #host4

"#" で始まる行はコメントとして解釈される。

shell operators
^^^^^^^^^^^^^^^
tomahawkはコマンドを実行する際、シェル(/bin/sh)を介して実行するため、 '|' (パイプ)や '&&'、'||'などのオペレータを使うことができる。 ::

  $ tomahawk -h host1,host2 'ps auxww | grep python'


OPTIONS
-------

-h, --hosts
^^^^^^^^^^^
コマンドを実行するリモートホストの名前を指定する。','で区切ることで複数のホストを指定することが可能。

-f, --hosts-files
^^^^^^^^^^^^^^^^^
リモートホストの名前が記載されたファイルを指定する。','で区切ることで複数のファイルを指定することが可能。
ファイルのフォーマットは下記の通り。 ::

  web01
  web02
  #web03
  web04

'#'で始まる行はコメントとして解釈されるので、無視される。

-l, --prompt-login-password
^^^^^^^^^^^^^^^^^^^^^^^^^^^
推奨されていない。代わりに -P/--prompt-password を使うこと。v0.6.0で削除される予定。

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
