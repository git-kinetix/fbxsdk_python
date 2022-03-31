#!/bin/bash

ifss="$IFS"
IFS=$'\n'
for a in $(ls -d /opt/python/cp3*/);do
  PATH=${a}bin/:$PATH ./build_wheels.sh
done

IFS="$ifss"
