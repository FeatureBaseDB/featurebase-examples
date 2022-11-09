FROM ubuntu:18.04

RUN apt-get -y update 
RUN apt-get -y upgrade 

RUN apt-get install wget -y

WORKDIR /featurebase

RUN wget https://github.com/FeatureBaseDB/featurebase/releases/download/v1.1.0-community/featurebase-v1.1.0-community-linux-arm64.tar.gz
RUN tar xvfz featurebase*.gz

EXPOSE 10101/tcp

CMD ["/featurebase/featurebase-v1.1.0-community-linux-arm64/featurebase","server"]
