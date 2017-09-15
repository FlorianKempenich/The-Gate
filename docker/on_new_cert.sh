#!/bin/bash

LETSENCRYPT_CERT_DIR=/https/letsencrypt/live/

while true
  do
    inotifywait -r -eCREATE $LETSENCRYPT_CERT_DIR > /output 2> /err
    echo
    echo "NEW CERTIFICATES DETECTED !!!!!!!!!!"
    echo "NEW CERTIFICATES DETECTED !!!!!!!!!!"
    echo "NEW CERTIFICATES DETECTED !!!!!!!!!!"
    echo "NEW CERTIFICATES DETECTED !!!!!!!!!!"
    echo
    $@
  done

echo "Exited the loop !!"
