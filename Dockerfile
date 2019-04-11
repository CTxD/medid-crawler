FROM ubuntu:18.04

LABEL MAINTAINER Casper Thomsen

COPY . /app/
WORKDIR /app/

RUN apt-get update

RUN apt-get -y install python3.7
RUN apt-get -y install python3-pip

RUN pip3 install -r requirements/dev
RUN python3 install.py

CMD ["python3", "main.py"]