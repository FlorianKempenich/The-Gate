#!/bin/sh

# Reloads the config by asking `nginx` in running container to do so.

CONTAINER=proxy
docker-compose exec $CONTAINER nginx -s reload
