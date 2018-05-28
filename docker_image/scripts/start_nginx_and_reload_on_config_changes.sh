#!/bin/bash

CERT_DIR=$LETSENCRYPT_DIR_IN_GATE/live/$LETSENCRYPT_CERT_NAME

FILE_CERT_ABS=$CERT_DIR/fullchain.pem
FILE_PRIVKEY_ABS=$CERT_DIR/privkey.pem
FILE_CONFIG_ABS=$CONFIG_DIR_IN_GATE/services.conf

function set_cert_location_on_service-base-conf {
    sed -i 's|CERTIFICATE_PATH_PLACEHOLDER|'$FILE_CERT_ABS'|g' /etc/nginx/services.base.conf
    sed -i 's|PRIVKEY_PATH_PLACEHOLDER|'$FILE_PRIVKEY_ABS'|g' /etc/nginx/services.base.conf
}
function watch_config_and_cert_for_changes {
    echo $FILE_CONFIG_ABS
    echo $FILE_CERT_ABS
    echo $FILE_PRIVKEY_ABS
    ./reload_nginx_on_file_change.sh $FILE_CONFIG_ABS &
    ./reload_nginx_on_file_change.sh $FILE_CERT_ABS &
    ./reload_nginx_on_file_change.sh $FILE_PRIVKEY_ABS &
}
function start_nginx {
    nginx -g 'daemon off;'
}


function main {
    set_cert_location_on_service-base-conf
    watch_config_and_cert_for_changes
    start_nginx
}
main



#### Deprecated for now ##########
#### Deprecated for now ##########
#### Deprecated for now ##########
#### Deprecated for now ##########
#### Deprecated for now ##########

## Utility functions ##########################################
# function generate_fake_certificates {
#     path_to_save_certificate=$1
#     path_to_save_privkey=$2
#
#     mkdir -p $(dirname $path_to_save_certificate)
#     mkdir -p $(dirname $path_to_save_privkey)
#
#     openssl req \
    #             -subj "/CN=fakedomain.com/O=FakeCompany./C=US" \
    #             -new -newkey rsa:2048 -days 365 -nodes -x509 \
    #             -keyout $path_to_save_privkey \
    #             -out $path_to_save_certificate
# }
## END - Utility functions ####################################

##################################################################
## If no existing certificates => Generate Temp/Fake ones       ##
##################################################################
# This allows `nginx` to start even before the real certificates are available.
# All websites will be served but a `NOT SECURE` warning will appear on the browser.
#
# This also allows `nginx` to serve the static content necessary to the initial
# certificate generation without having to comment out `servers` that need certificates
####if [ ! -e "$FILE_CERT_ABS" ] || [ ! -e "$FILE_PRIVKEY_ABS" ]
####then
####    generate_fake_certificates $FILE_CERT_ABS $FILE_PRIVKEY_ABS
####fi
##################################################################
## END - If no existing certificates => Generate Temp/Fake ones ##
##################################################################

