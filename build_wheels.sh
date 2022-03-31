./pull_reqs.sh

pip --verbose wheel .

LD_LIBRARY_PATH=${fbxsdkdir}/lib/gcc/x64/release/:$LD_LIBRARY_PATH auditwheel -v repair $(ls -1t fbx*.whl|head -1)
