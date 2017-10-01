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

# Load configuration
# Todo: Maybe make a bit more secure than that .... let's see
source ./config.env
check_exist "Service Configuration directory" $DIR_CONFIG
check_exist "\`services.conf\`" $DIR_CONFIG/services.conf
check_exist "Webroot directory" $DIR_WEBROOT
check_exist "Certificates base directory" $DIR_CERTIFICATES


