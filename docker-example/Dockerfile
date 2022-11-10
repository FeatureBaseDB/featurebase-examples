FROM ubuntu:18.04

RUN apt-get -y update 
RUN apt-get -y upgrade

RUN apt-get install wget -y
RUN apt-get install python3 -y
RUN apt-get install openjdk-11-jdk -y
RUN apt-get install python3-pip -y

WORKDIR /featurebase

# copy files
COPY featurebase.conf /featurebase
COPY schema.json /featurebase

# download and setup featurebase
RUN wget https://github.com/FeatureBaseDB/featurebase/releases/download/v1.1.0-community/featurebase-v1.1.0-community-linux-amd64.tar.gz
RUN tar xvfz featurebase*.gz
RUN mkdir /var/log/featurebase/

# cleanup tarballs
RUN rm featurebase*.tar.gz

# move directories around and set bits
RUN mkdir fb idk kafka
RUN mv featurebase-*/* fb
RUN mv idk-*/* idk
RUN chmod 755 idk/*

# ports
EXPOSE 10101/tcp

COPY start-processes.sh /featurebase

CMD ["/featurebase/start-processes.sh"]
# CMD ["/featurebase/fb/featurebase","server","--config","featurebase.conf"]


