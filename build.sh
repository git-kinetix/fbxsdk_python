#!/bin/bash

set -x

which auditwheel 

origdir=$(pwd)
scdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
builddir="$scdir"/build
fbxsdkdir="$builddir"/fbxsdk
fbxpydir="$builddir"/fbxpy
[ -d "$builddir" ] || mkdir "$builddir"

# Download fbxsdk and fbxsdk python bindings
while read l; do curl -L -O $l; done < "$scdir"/reqs.txt
ls -1 *.tar.gz|while read a;do tar -xvzf "$a" -C "$builddir";done
rm fbx*.tar.gz

# install fbxsdk
[ -d "$fbxsdkdir" ] || mkdir "$fbxsdkdir"
printf "yes\nn\n" |"$builddir"/fbx*fbxsdk_linux "$fbxsdkdir"

# install fbxsdk python bindings
[ -d "$fbxpydir" ] || mkdir "$fbxpydir"
printf "yes\nn\n" |"$builddir"/fbx*fbxpythonbindings_linux "$fbxpydir"

# patch sip files and library headers so that they compile with sip5
patch -p0 < patch

sip-wheel --verbose

auditwheel repair build/fbx/fbx*.whl
