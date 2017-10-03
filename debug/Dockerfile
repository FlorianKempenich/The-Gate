FROM ubuntu

RUN apt-get update && apt-get install -y \
    inotify-tools \
    procps \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir /sandbox
WORKDIR /sandbox

