#!/bin/bash

dir_to_watch=$1
cmd_to_run=${@:2}

while true
do
    # Block until change is detected (or error)
    inotifywait -r -eCREATE $dir_to_watch

    if [ $? == '0' ]; then
        # New certificates detected
        echo "NEW CERTIFICATES DETECTED !!!!!!!!!!"
        $cmd_to_run
    else
        # Error: Retry in 1s
        sleep 1
    fi
done

echo "Error !!! Watcher exited the loop !!"
