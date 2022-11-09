FROM ubuntu:18.04

RUN apt-get -y update 
RUN apt-get -y upgrade 

RUN apt-get install wget -y
RUN apt-get install python3 -y

WORKDIR /featurebase

COPY featurebase.conf /featurebase

RUN wget https://github.com/FeatureBaseDB/featurebase/releases/download/v1.1.0-community/featurebase-v1.1.0-community-linux-amd64.tar.gz
RUN tar xvfz featurebase*.gz
RUN mkdir /var/log/featurebase/

EXPOSE 10101/tcp

ENTRYPOINT ["/featurebase/featurebase-v1.1.0-community-linux-amd64/featurebase","server","--config","featurebase.conf"]
# ENTRYPOINT ["/usr/bin/python3", "-m", "http.server", "8000", "--bind", "0.0.0.0"] 

