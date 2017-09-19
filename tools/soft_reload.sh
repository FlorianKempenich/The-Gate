#!/bin/sh

# Reloads the CERTIFICATES by restarting nginx only
docker-compose exec proxy nginx -s reload
