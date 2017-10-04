#!/bin/bash

## Utility functions ##########################################
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
## END - Utility functions ####################################




##################################################################
##                             MAIN                             ##
##################################################################

##################################################################
## If no existing certificates => Generate Temp/Fake ones       ##
##################################################################
# This allows `nginx` to start even before the real certificates are available.
# All websites will be served but a `NOT SECURE` warning will appear on the browser.
#
# This also allows `nginx` to serve the static content necessary to the initial
# certificate generation without having to comment out `servers` that need certificates
if [ ! -e "$FILE_CERT_ABS" ] || [ ! -e "$FILE_PRIVKEY_ABS" ]
then
    generate_fake_certificates $FILE_CERT_ABS $FILE_PRIVKEY_ABS
fi
##################################################################
## END - If no existing certificates => Generate Temp/Fake ones ##
##################################################################


############################################################
## Set certificate location on `services.base.conf`       ##
############################################################
sed -i 's|CERTIFICATE_PATH_PLACEHOLDER|'$FILE_CERT_ABS'|g' /etc/nginx/services.base.conf
sed -i 's|PRIVKEY_PATH_PLACEHOLDER|'$FILE_PRIVKEY_ABS'|g' /etc/nginx/services.base.conf
############################################################
## END - Set certificate location on `services.base.conf` ##
############################################################


#####################################################################
## On new config, certificates or privkey ==> reload `nginx`       ##
#####################################################################
RELOAD_NGINX_CMD="nginx -s reload"

./watch_file.sh $FILE_CONFIG_ABS $RELOAD_NGINX_CMD &
./watch_file.sh $FILE_CERT_ABS $RELOAD_NGINX_CMD &
./watch_file.sh $FILE_PRIVKEY_ABS $RELOAD_NGINX_CMD &
#####################################################################
## END - On new config, certificates or privkey ==> reload `nginx` ##
#####################################################################


#########################
## Start `nginx`       ##
#########################
nginx -g 'daemon off;'
