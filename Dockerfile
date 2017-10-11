FROM python:3.6.3-stretch

RUN apt-get update && \
    apt-get install build-essential -y

ADD . /home
WORKDIR /home

ENTRYPOINT ["make", "run"]
