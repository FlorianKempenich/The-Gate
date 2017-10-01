#!/bin/bash

function check_directory_exist {
  docker run --rm -v"/:/hostroot" ubuntu ls /hostroot$2 > /dev/null 2>&1
  if ! [ "$?" == 0 ]; then
    echo ""
    echo "$1 \`$2\` could not be found."
    echo "Please check config!"
    echo ""
    exit 1
  fi
}

# Todo: Maybe make a bit more secure than that .... let's see
source ./config.env



check_directory_exist Root /
check_directory_exist Etc /etc
check_directory_exist "Stupid thing" asdf

