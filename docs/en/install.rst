How to install tomahawk
=======================

Requirements
------------

* python >= 2.4
* argparse (required only with python < 2.7)
* multiprocessing (required only with python < 2.6)
* pexpect
* pytest (required for testing)
* flexmock (required for testing)

Installation
------------

.. highlight:: bash

tomahawk distributions is in the `pypi <http://pypi.python.org/pypi/tomahawk/>`_, so the easiest way is using pip or easy_install ::

  $ sudo pip install tomahawk

or ::

  $ sudo easy_install tomahawk


Or you can use traditional way ::

  $ tar xvzf tomahawk-x.y.z.tar.gz
  $ cd tomahawk-x.y.z
  $ sudo python setup.py install

