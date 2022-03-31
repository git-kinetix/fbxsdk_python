FROM quay.io/pypa/manylinux2014_x86_64

COPY . /fbxsdkpy

CMD ./buildall.sh
