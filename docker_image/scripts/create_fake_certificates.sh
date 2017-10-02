#!/bin/bash

# TODO: Remove hardocded certificate location
# (get from domain, `letsencrypt` structure is fine .... this image is dedicated to `letsencrypt`)
# cd $CERT_PATH

openssl req \
        -subj "/CN=fakedomain.com/O=FakeCompany./C=US" \
        -new -newkey rsa:2048 -days 365 -nodes -x509 \
        -keyout $FILE_PRIVKEY_ABS \
        -out $FILE_CERT_ABS
