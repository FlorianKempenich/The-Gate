#!/bin/bash


# TODO: Remove hardocded certificate location
# (get from domain, `letsencrypt` structure is fine .... this image is dedicated to `letsencrypt`)
cd /https/letsencrypt/live/professionalbeginner.com

openssl req \
        -subj "/CN=fakedomain.com/O=FakeCompany./C=US" \
        -new -newkey rsa:2048 -days 365 -nodes -x509 \
        -keyout privkey.pem \
        -out fullchain.pem
