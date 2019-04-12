FROM ubuntu:18.04

LABEL MAINTAINER Casper Thomsen

COPY . /app/
WORKDIR /app/

RUN apt-get update

RUN apt-get -y install python3.7
RUN apt-get -y install python3-pip

RUN cp config.cfg.example config.cfg

RUN make install

CMD ["make", "main"]