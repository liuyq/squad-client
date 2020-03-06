FROM debian:buster-slim

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -q=2 && \
    apt-get install -q=2 --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        python3-yaml

WORKDIR /app
COPY . ./

RUN pip3 install -r requirements.txt
