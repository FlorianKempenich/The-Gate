#!/bin/bash

LETSENCRYPT_CERT_DIR=/https/letsencrypt/live/

while inotifywait -qqr -eCREATE $LETSENCRYPT_CERT_DIR
  do
    $@
  done

