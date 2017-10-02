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
CERT_PATH="${FILE_ABS%"$(basename $FILE_ABS)"}" # Temporary hack :)

echo
echo "Results:"
echo "FILE_ABS  ->  $FILE_ABS"
echo "CERT_PATH -> $CERT_PATH"
echo
echo "\$(dirname \$FILE_ABS) -> $(dirname $FILE_ABS)"
