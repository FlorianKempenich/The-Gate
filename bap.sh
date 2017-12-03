#!/bin/bash

docker build -t floriankempenich/the-gate .

if [ "$1" == "p" ]; then
  docker push floriankempenich/the-gate
fi

