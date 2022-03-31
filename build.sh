#!/bin/bash

set -x

which python
python --version

origdir=$(pwd)
scdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
builddir="$scdir"/build
fbxsdkdir="$builddir"/fbxsdk
fbxpydir="$builddir"/fbxpy
reqsfile="${scdir}"/reqs.txt
[ -d "$builddir" ] || mkdir "$builddir"

# download fbxsdk
if [ ! -d "$fbxsdkdir" ]
then
  mkdir "$fbxsdkdir"
  url=$(grep 'fbx.*fbxsdk' $reqsfile)
  file=${url##*/}
  tar="${fbxsdkdir}/${f}"
  curl -L -o "$tar" $url
  tar -xvzf "$tar" -C "$fbxsdkdir"
  printf "yes\nn\n" |"$fbxsdkdir"/fbx*fbxsdk_linux "$fbxsdkdir"
  # patch libfbxsdk.so because it is not linked against libxml2 and libz for some reason  
  patchelf --add-needed libz.so.1 ${fbxsdkdir}/lib/gcc/x64/release/libfbxsdk.so
  patchelf --add-needed libxml2.so.2 ${fbxsdkdir}/lib/gcc/x64/release/libfbxsdk.so
else
  echo "Skipping installation of fbxsdk because "$fbxsdkdir" exists"
fi

# download fbxsdk python bindings
if [ ! -d "$fbxpydir" ]
then
  mkdir "$fbxpydir"
  url=$(grep 'fbx.*fbxpythonbindings_linux' $reqsfile)
  file=${url##*/}
  tar="${fbxpydir}/${f}"
  curl -L -o "$tar" $url
  tar -xvzf "$tar" -C "$fbxpydir"
  printf "yes\nn\n"|"$fbxpydir"/fbx*fbxpythonbindings_linux "$fbxpydir"
  # patch sip files and library headers so that they compile with sip5
  patch -N -p0 < patch
else
  echo "Skipping installation of fbx python bindings because "$fbxpydir" exists"
fi

sip-wheel --verbose

LD_LIBRARY_PATH=${fbxsdkdir}/lib/gcc/x64/release/:$LD_LIBRARY_PATH auditwheel -v repair $(ls -1t fbx*.whl|head -1)
