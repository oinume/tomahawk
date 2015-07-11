.. -*- restructuredtext -*-

.. image:: https://img.shields.io/travis/oinume/tomahawk/hotfix/0.7.svg
    :target: https://travis-ci.org/oinume/tomahawk
    :alt: Build status

.. image:: https://img.shields.io/pypi/v/tomahawk.svg
    :target: https://pypi.python.org/pypi/tomahawk/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/tomahawk.svg
    :target: https://pypi.python.org/pypi/tomahawk/
    :alt: Downloads

.. image:: https://img.shields.io/github/license/oinume/tomahawk.svg
    :target: https://pypi.python.org/pypi/tomahawk/
    :alt: License

Examples
========

$ tomahawk -h host1,host2,host3 uptime

--> 'uptime' command is executed in host1, host2 and host3 as follows.

kazuhiro@host1 % uptime
22:41:27 up 10 days,  3:26,  1 users,  load average: 1.11, 1.13, 1.11 

kazuhiro@host2 % uptime
22:41:28 up 20 days,  4:26,  2 users,  load average: 2.11, 2.13, 2.11 

kazuhiro@host3 % uptime
22:41:29 up 30 days,  5:26,  3 users,  load average: 3.11, 3.13, 3.11 

$ tomahawk-rsync -h host1,host2,host3 test.py /tmp/test.py

--> 'test.py' is copied to host1, host2 and host3.

See more usages: http://readthedocs.org/docs/tomahawk/en/latest/


Documentation
=============
See http://readthedocs.org/docs/tomahawk/en/latest/


Changes
=======
See https://github.com/oinume/tomahawk/blob/master/docs/en/changes.rst


How to contribute
=================

Report a bug
------------
https://github.com/oinume/tomahawk/issues

Send a patch
------------
Fork, modify code, add tests, run tests, send pull request.


For developers
==============
Install tomahawk in develop mode. ::

  $ python setup.py develop

  or

  $ pip install -e .

Install following modules for testing. ::

  $ pip install requirements-dev.txt

Run unit tests ::

  $ py.test tests/internal/

