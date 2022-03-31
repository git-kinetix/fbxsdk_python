#!/bin/bash

ifss="$IFS"
IFS=$'\n'
for a in $(ls -d /opt/python/cp3*/);do
  PATH=${a}bin/:$PATH python -m pip install sip
  PATH=${a}bin/:$PATH ./build.sh
done

IFS="$ifss"
