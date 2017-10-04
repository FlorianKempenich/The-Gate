#!/bin/bash
################
# DEBUG        #
# TODO: Remove #
################
docker kill the-gate > /dev/null 2>&1
docker rm the-gate > /dev/null 2>&1
################
# END - DEBUG  #
# TODO: Remove #
################
function cleanup_trailing_slash { echo ${1%/}; }
function cleanup_leading_dotslash { echo ${1#./}; }
function full_path {
    echo $(cleanup_trailing_slash $1)/$(cleanup_leading_dotslash $2)
}
function check_exist {
    # Mounts the root on a docker image, and does the check on the image.
    #
    # That allow to check if file is present on Docker HOST,
    # even when the HOST is a remote machine.
    docker run --rm -v"/:/hostroot" alpine ls /hostroot$2 > /dev/null 2>&1
    if ! [ "$?" == 0 ]; then
        echo ""
        echo "$1: \`$2\` could not be found."
        echo "==> Please check config!"
        echo ""
        exit 1
    fi
}


######################
##       MAIN       ##
######################

## Load configuration ###########################################
# Todo: Maybe make a bit more secure than that .... let's see
source ./config.env

DIR_CONFIG=$(cleanup_trailing_slash $DIR_CONFIG)
DIR_WEBROOT=$(cleanup_trailing_slash $DIR_WEBROOT)
DIR_CERTIFICATES=$(cleanup_trailing_slash $DIR_CERTIFICATES)

DIR_CONFIG_IN_CONTAINER="/etc/nginx/the-gate-services/"
DIR_WEBROOT_IN_CONTAINER="/https/webroot/"
DIR_CERTIFICATES_IN_CONTAINER="/https/certificates/"

FILE_CONFIG_ABS_IN_CONTAINER=$(full_path $DIR_CONFIG_IN_CONTAINER "services.conf")
FILE_CERT_ABS_IN_CONTAINER=$(full_path $DIR_CERTIFICATES_IN_CONTAINER $FILE_CERT)
FILE_PRIVKEY_ABS_IN_CONTAINER=$(full_path $DIR_CERTIFICATES_IN_CONTAINER $FILE_PRIVKEY)
## End - Load configuration #####################################


## Check config present on host #################################
check_exist "Service Configuration directory" $DIR_CONFIG
check_exist "\`services.conf\`" $DIR_CONFIG/services.conf
check_exist "Webroot directory" $DIR_WEBROOT
check_exist "Certificates base directory" $DIR_CERTIFICATES
## End - Check config present on host ###########################


# Start The Gate
docker run \
       -d \
       -p "80:80" \
       -p "443:443" \
       --network="host" \
       --restart=always \
       --name=the-gate \
       -e FILE_CONFIG_ABS=$FILE_CONFIG_ABS_IN_CONTAINER \
       -e FILE_CERT_ABS=$FILE_CERT_ABS_IN_CONTAINER \
       -e FILE_PRIVKEY_ABS=$FILE_PRIVKEY_ABS_IN_CONTAINER \
       -v "$DIR_WEBROOT:$DIR_WEBROOT_IN_CONTAINER" \
       -v "$DIR_CERTIFICATES:$DIR_CERTIFICATES_IN_CONTAINER" \
       -v "$DIR_CONFIG:$DIR_CONFIG_IN_CONTAINER" \
       shockn745/the-gate
