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
tomahawkは引数のコマンドを`ssh'を介して実行する。-o/--ssh-options でsshを実行する際のオプションを指定できる他、$HOME/.ssh/config で柔軟な設定が可能である。

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
最初のSSH認証のためのパスワードを尋ねる。

--login-password-stdin
^^^^^^^^^^^^^^^^^^^^^^
SSHの認証パスワードを尋ねる代わりに標準入力から読み取る。

-s, --prompt-sudo-password
^^^^^^^^^^^^^^^^^^^^^^^^^^
sudoを含むコマンドを実行する際、sudoのためのパスワードを尋ねる。

-c, --continue-on-error
^^^^^^^^^^^^^^^^^^^^^^^
コマンドが失敗した場合、デフォルトでは tomahawk は実行をそのホストでストップするが、このオプションを指定すると、コマンドが失敗した場合でも処理を継続する。

-p, --parallel
^^^^^^^^^^^^^^
リモートホストでのコマンド実行を並列で実行するためのプロセス数を指定する。(デフォルトは1)
CPUコアが複数ある場合 --parallel=2 などとすると処理速度が向上するであろう。
このオプションを指定した場合、リモートホストに対してコマンドを実行する順番は保証されなくなる。

-t, --timeout
^^^^^^^^^^^^^
タイムアウト秒数を指定する。

--expect-timeout
^^^^^^^^^^^^^^^^
推奨されていない。代わりに -t/--timeout を使うこと。v0.6.0で削除される予定。

-u, --ssh-user
^^^^^^^^^^^^^^
sshでコマンドを実行する際のユーザ名を指定する。デフォルトはログインしているユーザ。

-o, --ssh-options
^^^^^^^^^^^^^^^^^
sshでコマンドを実行する際のオプションを指定する。

--output-format
^^^^^^^^^^^^^^^
コマンドの出力フォーマットを指定する。
デフォルトは '${user}@${host} % ${command}\n${output}\n'


SEE ALSO
--------
* :manpage:`tomahawk-rsync(1)`
* :manpage:`ssh(1)`
* :manpage:`scp(1)`
