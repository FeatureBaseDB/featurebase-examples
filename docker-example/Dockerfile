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
COPY set-schema.json /featurebase

# download and setup featurebase
RUN wget https://github.com/FeatureBaseDB/featurebase/releases/download/v3.30.0/featurebase-v3.30.0-linux-amd64.tar.gz
RUN tar xvfz featurebase*.gz
RUN mkdir /var/log/featurebase/

# download and run kafka
RUN wget https://downloads.apache.org/kafka/3.3.1/kafka_2.13-3.3.1.tgz
RUN tar xvfz kafka_2.13-3.3.1.tgz

# cleanup tarballs
RUN rm featurebase*.tar.gz
RUN rm kafka*.tgz

# move directories around and set bits
RUN mkdir fb idk kafka
RUN mv featurebase-*/* fb
RUN mv idk-*/* idk
RUN mv kafka_*/* kafka
RUN rm -rf featurebase-* idk-* kafka_*
RUN chmod 755 idk/*

# ports
EXPOSE 10101/tcp
EXPOSE 20101/tcp

RUN echo "rebuild"

COPY start-processes.sh /featurebase

CMD ["/featurebase/start-processes.sh"]
# CMD ["/featurebase/fb/featurebase","server","--config","featurebase.conf"]


