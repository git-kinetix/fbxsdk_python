#!/bin/bash

set -x

origdir=$(pwd)
scdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
builddir="$scdir"/build
sipdir="$builddir/sip-4.19.3"
fbxsdkdir="$builddir"/fbxsdk
fbxpydir="$builddir"/fbxpy
sipinstalldir="$builddir"/sipinstall
[ -d "$builddir" ] || mkdir "$builddir"

wget -nc -i "$scdir"/reqs.txt
ls -1 *.tar.gz|while read a;do tar -xvzf "$a" -C "$builddir";done
rm fbx*.tar.gz

[ -d "$fbxsdkdir" ] || mkdir "$fbxsdkdir"
printf "yes\nn\n" |"$builddir"/fbx*fbxsdk_linux "$fbxsdkdir"

[ -d "$fbxpydir" ] || mkdir "$fbxpydir"
printf "yes\nn\n" |"$builddir"/fbx*fbxpythonbindings_linux "$fbxpydir"

[ -d "$sipinstalldir" ] || mkdir "$sipinstalldir"
cd "$sipdir"
python3  "${sipdir}"/configure.py -b "$sipinstalldir" -d "$sipinstalldir" -e "$sipinstalldir" --pyidir="$sipinstalldir" --sip-module="fbxsip"
make --debug -C"${sipdir}"
make install --debug -C"${sipdir}"
cd "$origdir"

patch -p0 < patch

cp "$scdir/PythonBindings.py" "$fbxpydir"
FBXSDK_ROOT="$fbxsdkdir" SIP_ROOT="$sipdir" python3 "$fbxpydir"/PythonBindings.py Python3_x64

pyvers=$(python3 --version 2>&1 | cut -d' ' -f2)
pyvers=${pyvers%.*}
pyvers=${pyvers//./}
fbxdir="$scdir"/fbxsdkpy-cp${pyvers}-gnu_linux_x64
[ -d "$fbxdir" ] || mkdir "$fbxdir"
cp "$fbxpydir"/build/Distrib/site-packages/fbx/* "$fbxdir"
cp "$sipinstalldir"/fbxsip.so "$fbxdir"
