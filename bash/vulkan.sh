#!/bin/bash

wine=$1
url=$2
name=$3

rm -r download
mkdir download
wget -P download "$url"
tar -xf download/"$name" -C download

dir=$(tar -tf download/"$name" | head -1)
var=$(WINEPREFIX="$wine" download/"$dir"*setup* install)
echo "$var"
