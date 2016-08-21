FROM ubuntu:16.04
RUN apt-get update && apt-get install -y python3.5 python3.5-dev python3-pip openssh-client openssh-server
RUN test -e ~/.ssh/id_rsa || ssh-keygen  -t rsa -f ~/.ssh/id_rsa -N ''
RUN cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys
RUN echo "Host localhost" > ~/.ssh/config && echo "StrictHostKeyChecking no" >> ~/.ssh/config
ADD . /root/tomahawk
RUN cd /root/tomahawk && python3 setup.py develop
