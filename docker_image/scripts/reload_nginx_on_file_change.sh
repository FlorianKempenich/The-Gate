#!/bin/bash

####################################################
# Watch for a file and reload nginx if file is:    #
#                                                  #
# - CREATED (or Recreated)                         #
# - MODIFIED                                       #
#                                                  #
#                                                  #
# USAGE:                                           #
# ------                                           #
#                                                  #
#     ./reload_nginx_on_file_change.sh FILE        #
#                                                  #
####################################################
function reload_nginx {
    echo "RELOADING: NginX configuration"
    nginx -s reload
}

file_to_watch=$1
dir_to_watch=$(dirname $file_to_watch)
while true
do
    # Block until change is detected (or error)
    file_changed=$(inotifywait -r -eCREATE -eMODIFY --format="%f" $dir_to_watch)

    if [ $? != '0' ]; then
        # Error: Wait 1s before reloading and re-trying
        echo "Error: Retrying to watch \`$file_to_watch\` in 1s"
        sleep 1
    elif [ "$file_changed" == "$(basename $file_to_watch)" ]; then
        # Watched file changed, or created (or re-created)
        echo "FILE CHANGED: \`$file_to_watch\`"
    else
        echo "FILE CHANGED: File changed is not the one watched: file_changed=\`$file_changed\`"
        echo "Reloading anyway."
    fi

    reload_nginx
done

echo "Error !!! Watcher exited the loop !!"
