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

OPTIONS
-------
These programs follow the usual GNU command line syntax, with long options starting with two dashes ('--').
A summary of options is included below.
For a complete description, see the Info files.

-h, --hosts
^^^^^^^^^^^
rsyncコマンドを実行するリモートホストの名前を指定する。','で区切ることで複数のホストを指定することが可能。

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

-P, --prompt-login-password
^^^^^^^^^^^^^^^^^^^^^^^^^^^
(rsyncで使用する)SSH認証のためのパスワードを尋ねる。

--login-password-stdin
^^^^^^^^^^^^^^^^^^^^^^
SSHの認証パスワードを尋ねる代わりに標準入力から読み取る。

-c, --continue-on-error
^^^^^^^^^^^^^^^^^^^^^^^
rsyncが失敗した場合、デフォルトでは tomahawk-rsync は実行をそのホストでストップするが、このオプションを指定すると、コマンドが失敗した場合でも処理を継続する。

-p, --parallel
^^^^^^^^^^^^^^
リモートホストでのrsyncを並列で実行するためのプロセス数を指定する。(デフォルトは1)
CPUコアが複数ある場合 --parallel=2 などとすると処理速度が向上するであろう。
このオプションを指定した場合、リモートホストに対してrsyncを実行する順番は保証されなくなる。

-t, --timeout
^^^^^^^^^^^^^
タイムアウト秒数を指定する。

--output-format
^^^^^^^^^^^^^^^
rsyncコマンドの出力フォーマットを指定する。
デフォルトは '${user}@${host} % ${command}\n${output}\n'

-u, --rsync-user
^^^^^^^^^^^^^^^^
Specifies rsync user. The default is a current logged in user.

-o, --rsync-options
^^^^^^^^^^^^^^^^^^^
rsyncでコマンドを実行する際のオプションを指定する。デフォルトは'-av'

-m, --mirror-mode
^^^^^^^^^^^^^^^^^
'push'または'pull'を指定する。
'pull'を指定するとリモートホストからローカルにファイルをコピーする。
デフォルトは'push'


SEE ALSO
--------
* :manpage:`tomahawk(1)`
* :manpage:`ssh(1)`
* :manpage:`rsync(1)`
