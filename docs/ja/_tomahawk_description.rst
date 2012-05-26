.. highlight:: bash

:program:`tomahawk` is a program that enables to execute a command into many hosts. ::

  $ tomahawk -h host1,host2,host3 uptime

---> 'uptime' command will be executed in host1, host2, and host3 with following output. ::

  oinume@host1 % uptime
  22:41:27 up 10 days,  3:26,  1 users,  load average: 1.11, 1.13, 1.11 
  
  oinume@host2 % uptime
  22:41:28 up 20 days,  4:26,  2 users,  load average: 2.11, 2.13, 2.11 
  
  oinume@host3 % uptime
  22:41:29 up 30 days,  5:26,  3 users,  load average: 3.11, 3.13, 3.11 
