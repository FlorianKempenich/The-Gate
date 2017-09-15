#!/bin/sh

CERT_PATH=/https/letsencrypt/live/professionalbeginner.com


# IF NO CERTIFICATES FOUND => Create Fake Certificates:
# -----------------------------------------------------
#
# This allows `nginx` to start even before the real certificates are available.
# All websites will be served but a `NOT SECURE` warning will appear on the browser.
#
# This also allows `nginx` to serve the static content necessary to the initial
# certificate generation without having to comment out `servers` that need certificates
if [ ! -e "$CERT_PATH/fullchain.pem" ] || [ ! -e "$CERT_PATH/privkey.pem" ]
then
    ./create_fake_certificates.sh
fi


# On new certificates, reload `nginx`
./on_new_cert.sh nginx -s reload &

# Start `nginx`
nginx -g 'daemon off;'
