How to install tomahawk
=======================

必要なソフトウェア
------------------

* python >= 2.4
* argparse (python-2.7未満の場合)
* multiprocessing (python-2.6未満の場合)
* pexpect
* pytest (required for testing)
* mock (required for testing)

インストール
------------

.. highlight:: bash

tomahawk のディストリビューションは `pypi <http://pypi.python.org/pypi/tomahawk/>`_ にあるので、pip または easy_install を使うと簡単にインストールできる。::

  $ sudo pip install tomahawk

または ::

  $ sudo easy_install tomahawk


もしくは下記でもインストールできる ::

  $ tar xvzf tomahawk-x.y.z.tar.gz
  $ cd tomahawk-x.y.z
  $ sudo python setup.py install

