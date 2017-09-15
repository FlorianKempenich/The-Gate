#!/bin/sh

# On new certificates, reload `nginx`
./on_new_cert.sh nginx -s reload &

# Start `nginx`
nginx -g 'daemon off;'
