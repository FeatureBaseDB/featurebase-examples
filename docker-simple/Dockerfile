FROM ubuntu:18.04

RUN apt-get -y update 
RUN apt-get -y upgrade
RUN apt-get install wget -y

WORKDIR /featurebase

# copy files
COPY featurebase.conf /featurebase

# download and setup featurebase
RUN wget https://github.com/FeatureBaseDB/featurebase/releases/download/v3.26.0/featurebase-v3.26.0-linux-amd64.tar.gz
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

# ports
EXPOSE 10101/tcp
EXPOSE 20101/tcp

ENTRYPOINT ["/featurebase/fb/featurebase","server","--config","featurebase.conf", "--sql.endpoint-enabled"]