#!/bin/bash


function generate_fake_certificates {
    path_to_save_certificate=$1
    path_to_save_privkey=$2

    mkdir -p $(dirname $path_to_save_certificate)
    mkdir -p $(dirname $path_to_save_privkey)

    openssl req \
            -subj "/CN=fakedomain.com/O=FakeCompany./C=US" \
            -new -newkey rsa:2048 -days 365 -nodes -x509 \
            -keyout $path_to_save_privkey \
            -out $path_to_save_certificate
}


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
    generate_fake_certificates $FILE_CERT_ABS $FILE_PRIVKEY_ABS
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


# Set certificate location on `services.base.conf`
sed -i 's|CERTIFICATE_PATH_PLACEHOLDER|'$FILE_CERT_ABS'|g' /etc/nginx/services.base.conf
sed -i 's|PRIVKEY_PATH_PLACEHOLDER|'$FILE_PRIVKEY_ABS'|g' /etc/nginx/services.base.conf

# TODO: Remove CERT_PATH hack
CERT_PATH=$(dirname $FILE_CERT_ABS)
# On new certificates, reload `nginx`
./on_new_cert.sh nginx -s reload &

# Start `nginx`
nginx -g 'daemon off;'
