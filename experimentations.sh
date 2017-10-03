#!/bin/bash

#Experimentation
dir=/https/letsencrypt/
dir_noslash=/https/letsencrypt

file=./live/the-ecosystem.xyz/fullchain.pem
file_nodot=live/the-ecosystem.xyz/fullchain.pem


function full_path {
    echo ${1%/}/${2#./}
}

echo $(full_path $dir         $file      )
echo $(full_path $dir_noslash $file      )
echo $(full_path $dir         $file_nodot)
echo $(full_path $dir_noslash $file_nodot)

FILE_ABS=$(full_path $dir $file)

echo
echo "Results:"
echo "FILE_ABS  ->  $FILE_ABS"
echo
echo "\$(dirname \$FILE_ABS) -> $(dirname $FILE_ABS)"

hey=/https/letsencrypt/live/the-ecosystem.xyz/fullchain.pem
hey2=/https/letsencrypt/live/the-ecosystem.xyz/asdf.pem
boom=/https/letsencrypt/live/another-dir/fullchain.pem

function same_basedir {
    if [ "$(dirname $1)" == "$(dirname $2)" ]; then
        echo true
    else
        echo false
    fi
}

echo "echo same_basedir \$hey \$hey2 ==> "$(same_basedir $hey $hey2)
echo "echo same_basedir \$hey \$boom ==> "$(same_basedir $hey $boom)
echo "echo same_basedir \$hey2 \$boom ==> "$(same_basedir $hey2 $boom)

if [ "$(same_basedir $hey $hey2)" == true ]; then
    echo IT WORKS
fi

function watch_file_and_exec_cmd {
    file=$1
    cmd=${@:2}

    echo "file: $file"
    echo "cmd: $cmd"
    echo "cmd: and this is a command"
}

watch_file_and_exec_cmd ./hello_this_is_a_file and this is a command

