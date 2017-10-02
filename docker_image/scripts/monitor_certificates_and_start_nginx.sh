#!/bin/bash

function same_basedir {
    if [ "$(dirname $1)" == "$(dirname $2)" ]; then
        echo true
    else
        echo false
    fi
}

# IF NO CERTIFICATES FOUND => Create Fake Certificates:
# -----------------------------------------------------
#
# This allows `nginx` to start even before the real certificates are available.
# All websites will be served but a `NOT SECURE` warning will appear on the browser.
#
# This also allows `nginx` to serve the static content necessary to the initial
# certificate generation without having to comment out `servers` that need certificates

if [ ! -e "$FILE_CERT_ABS" ] || [ ! -e "$FILE_PRIVKEY_ABS" ]
then
    mkdir -p $(dirname $FILE_CERT_ABS)
    mkdir -p $(dirname $FILE_PRIVKEY_ABS)
    ./create_fake_certificates.sh
fi

if [ "$(same_basedir $FILE_CERT_ABS $FILE_PRIVKEY_ABS)" == true ]; then
    # Setup a single watch for both certificate files
    echo todo
else
    # Setup one watch for each certificate directory
    echo todo
fi
########### OOOOOOOOOOOORRRRRRRRRRRRRRRR !!!!!!!!!!!!!!!!!
########### Instead of watching directory =========> WATCH FILE DIRECTLY.
########### Now we can since we have the full name of it.


# TODO: Remove CERT_PATH hack
CERT_PATH=$(dirname $FILE_CERT_ABS)
# Set certificate location on `services.base.conf`
sed -i 's|CERTIFICATE_PATH_PLACEHOLDER|'$CERT_PATH'|g' /etc/nginx/services.base.conf

# On new certificates, reload `nginx`
./on_new_cert.sh nginx -s reload &

# Start `nginx`
nginx -g 'daemon off;'
