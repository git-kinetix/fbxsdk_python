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
  url=$(grep 'fbx.*fbxsdk' $reqsfile|cut -d';' -f 2)
  file=${url##*/}
  tar="${fbxsdkdir}/${file}"
  curl -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0' -L -o "$tar" $url
  tar -xvzf "$tar" -C "$fbxsdkdir"
  printf "yes\nn\n" |"$fbxsdkdir"/fbx*fbxsdk_linux "$fbxsdkdir" >/dev/null 2>&1
  # patch libfbxsdk.so because it is not linked against libxml2 and libz for some reason  
  chmod 777 ${fbxsdkdir}/lib/gcc/x64/release/libfbxsdk.so
  patchelf --add-needed libz.so.1 ${fbxsdkdir}/lib/gcc/x64/release/libfbxsdk.so
  patchelf --add-needed libxml2.so.2 ${fbxsdkdir}/lib/gcc/x64/release/libfbxsdk.so
  mv "${fbxsdkdir}/lib/gcc" "${fbxsdkdir}/lib/all"
else
  echo "Skipping installation of fbxsdk because "$fbxsdkdir" exists"
fi

# download fbxsdk python bindings
if [ ! -d "$fbxpydir" ]
then
  mkdir "$fbxpydir"
  url=$(grep 'fbx.*fbxpythonbindings_linux' $reqsfile|cut -d';' -f 2)
  file=${url##*/}
  tar="${fbxpydir}/${file}"
  curl -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0' -L -o "$tar" $url
  tar -xvzf "$tar" -C "$fbxpydir"
  printf "yes\nn\n"|"$fbxpydir"/fbx*fbxpythonbindings_linux "$fbxpydir" >/dev/null 2>&1

  # patch sip files and library headers so that they compile with sip5
  patch -N -p0 < patch
  
else
  echo "Skipping installation of fbx python bindings because "$fbxpydir" exists"
fi
