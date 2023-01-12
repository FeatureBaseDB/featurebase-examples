FROM ubuntu:18.04

RUN apt-get -y update 
RUN apt-get -y upgrade
RUN apt-get install wget -y
RUN apt-get install net-tools -y
RUN apt-get install dnsutils -y
RUN apt-get install iputils-ping -y

WORKDIR /featurebase

# copy files
COPY sample.csv /featurebase
COPY start.sh /featurebase

# download and setup featurebase
RUN wget https://github.com/FeatureBaseDB/featurebase/releases/download/v3.27.0/featurebase-v3.27.0-linux-amd64.tar.gz
RUN tar xvfz featurebase*.gz
RUN mkdir /var/log/featurebase/

# cleanup tarballs
RUN rm featurebase*.tar.gz

# move directories around and set bits
RUN mkdir fb idk
RUN mv featurebase-*/* fb
RUN mv idk-*/* idk
RUN rm -rf featurebase-* idk-*
RUN chmod 755 idk/*

# for running or shelling
ENTRYPOINT ["/bin/bash", "start.sh"]
