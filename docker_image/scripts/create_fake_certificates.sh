#!/bin/bash


# TODO: Remove hardocded certificate location
# (get from domain, `letsencrypt` structure is fine .... this image is dedicated to `letsencrypt`)
cd CERTIFICATE_PATH_PLACEHOLDER

openssl req \
        -subj "/CN=fakedomain.com/O=FakeCompany./C=US" \
        -new -newkey rsa:2048 -days 365 -nodes -x509 \
        -keyout privkey.pem \
        -out fullchain.pem