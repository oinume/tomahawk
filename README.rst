tomahawk
========
A simple ssh wrapper for executing a command to many hosts.

.. image:: https://secure.travis-ci.org/oinume/tomahawk.png?branch=0.5-hotfix

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

Bug report
==========
https://github.com/oinume/tomahawk/issues
