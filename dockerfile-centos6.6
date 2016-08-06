FROM centos:6.6
RUN yum install -y epel-release && yum install --enablerepo=epel -y python python-devel python-pip openssh-clients openssh-server
RUN test -e ~/.ssh/id_rsa || ssh-keygen  -t rsa -f ~/.ssh/id_rsa -N ''
RUN cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys
RUN echo "Host localhost" > ~/.ssh/config && echo "StrictHostKeyChecking no" >> ~/.ssh/config
ADD . /root/tomahawk
RUN cd /root/tomahawk && python setup.py develop
