#!/bin/bash

docker build -t shockn745/the-gate --file=./docker_image/NginxDockerfile . && \
    docker push shockn745/the-gate

