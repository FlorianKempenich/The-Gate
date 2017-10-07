#!/bin/bash
CONTAINER_NAME=the-gate

docker kill $CONTAINER_NAME && docker rm $CONTAINER_NAME

if [ $? == '0' ]; then
    echo " ________________________________ "
    echo "|                                |"
    echo "| The-Gate stopped successfully! |"
    echo "|________________________________|"
else
    echo " __________________________________________________ "
    echo "|                                                  |"
    echo "| A problem happened while trying to stop The-Gate |"
    echo "|__________________________________________________|"
    echo
fi

