#!/bin/bash

#DOCKER_IMG=floriankempenich/the-gate
DOCKER_IMG=floriankempenich/the-gate:debug

docker build -t $DOCKER_IMG .

if [ "$1" == "p" ]; then
  docker push $DOCKER_IMG
fi

