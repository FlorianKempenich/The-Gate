#!/bin/bash

####################################################
# Watch for a file and execute the cmd if file is: #
#                                                  #
# - CREATED (or Recreated)                         #
# - MODIFIED                                       #
#                                                  #
#                                                  #
# USAGE:                                           #
# ------                                           #
#                                                  #
#     watch_file.sh FILE CMD_TO_RUN                #
#                                                  #
####################################################

file_to_watch=$1
cmd_to_run=${@:2}

dir_to_watch=$(dirname $file_to_watch)
while true
do
    # Block until change is detected (or error)
    file_changed=$(inotifywait -r -eCREATE -eMODIFY --format="%f" $dir_to_watch)

    if [ $? != '0' ]; then
        # Error: Retry in 1s
        sleep 1
    elif [ "$file_changed" == "$(basename $file_to_watch)" ]; then
        # Watched file changed, or created (or re-created)
        $cmd_to_run
    fi
done

echo "Error !!! Watcher exited the loop !!"
