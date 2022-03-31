#!/bin/bash

set -x

which python
python --version

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
[ -d "$fbxsdkdir" ] || (mkdir "$fbxsdkdir" && printf "yes\nn\n" |"$builddir"/fbx*fbxsdk_linux "$fbxsdkdir")

# install fbxsdk python bindings
[ -d "$fbxpydir" ] || (mkdir "$fbxpydir" && printf "yes\nn\n" |"$builddir"/fbx*fbxpythonbindings_linux "$fbxpydir")

# patch sip files and library headers so that they compile with sip5
patch -p0 < patch

# patch libfbxsdk.so because it is not linked against libxml2 and libz for some reason  
patchelf --add-needed libz.so.1 ${fbxsdkdir}/lib/gcc/x64/release/libfbxsdk.so
patchelf --add-needed libxml2.so.2 ${fbxsdkdir}/lib/gcc/x64/release/libfbxsdk.so

sip-wheel --verbose

LD_LIBRARY_PATH=$(pwd)/build/fbxsdk/lib/gcc/x64/release/:$LD_LIBRARY_PATH auditwheel -v repair $(ls -1t fbx*.whl|head -1)
