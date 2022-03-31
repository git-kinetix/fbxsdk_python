pip --verbose wheel .

auditwheel -v repair $(ls -1t fbx*.whl|head -1)
