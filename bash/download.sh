#!/bin/bash

url=$1

rm -r download
mkdir download

wget -P download "$url"