#!/bin/bash

function check_exist {
  docker run --rm -v"/:/hostroot" alpine ls /hostroot$2 > /dev/null 2>&1
  if ! [ "$?" == 0 ]; then
    echo ""
    echo "$1: \`$2\` could not be found."
    echo "==> Please check config!"
    echo ""
    exit 1
  fi
}


################
# DEBUG        #
# TODO: Remove #
################
docker kill the-gate
docker rm the-gate
################
# END - DEBUG  #
# TODO: Remove #
################

# Load configuration
# Todo: Maybe make a bit more secure than that .... let's see
source ./config.env
# TODO: Uncomment when done (too slow during debug)
# check_exist "Service Configuration directory" $DIR_CONFIG
# check_exist "\`services.conf\`" $DIR_CONFIG/services.conf
# check_exist "Webroot directory" $DIR_WEBROOT
# check_exist "Certificates base directory" $DIR_CERTIFICATES


# TODO FIX the use of CERT_PATH, replace with $DIR_CERTIFICATES & file relative to that.
# Right now CERT_PATH represent the folder where `fullchain` and `privkey` directly are.
# This folder is IN THE DOCKER IMAGE/CONTAINER !!!!

# Start The Gate
docker run \
       -d \
       -p "80:80" \
       -p "443:443" \
       --network="host" \
       --restart=always \
       --name=the-gate \
       -e CERT_PATH="/https/certificates/whatever" \
       -v "$DIR_WEBROOT:/https/webroot/" \
       -v "$DIR_CERTIFICATES:/https/certificates/" \
       -v "$DIR_CONFIG:/etc/nginx/the-gate-services/" \
       shockn745/the-gate
