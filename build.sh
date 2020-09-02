#!/bin/sh

set -x

origdir=$(pwd)
cd $(dirname $0)
scdir=$(pwd)
builddir="$scdir"/build
[ -d "$builddir" ] || mkdir "$builddir"

cd "$builddir"

wget -nc -i "$scdir"/reqs.txt
cp ${scdir}/sip*.tar.gz "${builddir}"
ls -1 *.tar.gz|xargs -L 1 tar -xvf
rm *.tar.gz

fbxsdkdir="$builddir"/fbxsdk
mkdir "$fbxsdkdir"
printf "yes\nn\n" |./fbx*fbxsdk_linux "$fbxsdkdir"

fbxpydir="$builddir"/fbxpy
mkdir "$fbxpydir" 2>/dev/null
printf "yes\nn\n" |./fbx*fbxpythonbindings_linux "$fbxpydir"

sipdir="$builddir/sip-4.19.3"
cd "$sipdir"
sipinstalldir="$builddir"/sipinstall
mkdir "$sipinstalldir"
python3 configure.py -b "$sipinstalldir" -d "$sipinstalldir" -e "$sipinstalldir" --pyidir="$sipinstalldir"
make
make install

cd "$fbxpydir"
cp "$scdir/PythonBindings.py" .
export FBXSDK_ROOT="$fbxsdkdir"
export SIP_ROOT="$sipdir"
python3 PythonBindings.py Python3_x64

fbxdir="$scdir"/fbx
[ -d "$fbxdir" ] || mkdir "$fbxdir"
cp "$fbxpydir"/build/Distrib/site-packages/fbx/* "$fbxdir"
cp "$sipinstalldir"/sip.so "$fbxdir"

cd "$origdir"
