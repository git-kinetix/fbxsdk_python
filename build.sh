#!/bin/sh

set -xe

origdir=$(pwd)
cd $(dirname $0)
scdir=$(pwd)
builddir="$scdir"/build
[ -d "$builddir" ] || mkdir "$builddir"

cd "$builddir"

wget -i "$scdir"/reqs.txt
ls -1 *.tar.gz|xargs -L 1 tar -xvf
rm *.tar.gz

fbxsdkdir=fbxsdk
mkdir $fbxsdkdir
./fbx*fbxsdk_linux $fbxsdkdir

fbxpydir=fbxpy
mkdir $fbxpydir
./fbx*fbxpythonbindings_linux $fbxpydir

sipdir="sip-4.19.3"
cd $sipdir
python3 configure.py
make
make install

cd "$builddir/$fbxpydir"
cp "$scdir/PythonBindings.py" .
export FBXSDK_ROOT="${builddir}/$fbxsdkdir"
export SIP_ROOT="${builddir}/$sipdir"
python3 PythonBindings.py Python3_x64


cd "$origdir"
