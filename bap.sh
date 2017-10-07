#!/bin/bash

docker build -t shockn745/the-gate .

if [ "$1" == "p" ]; then
  docker push shockn745/the-gate
fi

