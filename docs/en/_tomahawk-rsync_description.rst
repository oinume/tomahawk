.. highlight:: bash

:program:`tomahawk-rsync` is a program that enables to copy files <into/from> many hosts. ::

  $ tomahawk-rsync -h host1,host2,host3 test.py /tmp/test.py

---> 'test.py' is copied to host1, host2 and host3. ::

  $ tomahawk-rsync -f web.list /usr/local/apache2/conf/httpd.conf /tmp/httpd.conf

---> 'httpd.conf' is copied to hosts which listed in 'web.list'. ::

  $ tomahawk-rsync -h host1,host2 -m pull /usr/local/apache2/conf/httpd.conf /tmp/conf/

---> 'httpd.conf' is copied from host1 and host2 to local directory /tmp/conf as 'host1__httpd.conf' and 'host2__httpd.conf'.
