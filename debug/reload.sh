#!/bin/bash

docker kill debug
docker run \
       --rm \
       -d \
       --name=debug \
       -v "$(pwd):/sandbox" \
       debug tail -f /dev/null
