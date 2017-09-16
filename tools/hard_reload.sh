#!/bin/sh

# Reloads the config by restarting the container
# Can also be used to start the service.
docker-compose up --build --force-recreate --timeout 0 -d
