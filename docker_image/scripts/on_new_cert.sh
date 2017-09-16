#!/bin/bash

LETSENCRYPT_CERT_DIR=/https/letsencrypt/live/professionalbeginner.com

while true
  do
    # Block until change is detected (or error)
    inotifywait -r -eCREATE $LETSENCRYPT_CERT_DIR
    if [ $? == '0' ]; then
        # New certificates detected
        echo "NEW CERTIFICATES DETECTED !!!!!!!!!!"
        $@
    else
        # Error: Retry in 1s
        sleep 1
    fi
  done

echo "Exited the loop !!"
