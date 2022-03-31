FROM quay.io/pypa/manylinux2014_x86_64

ARG pass

VOLUME /build

WORKDIR /build

RUN yum -y install libxml2-devel zlib-devel

CMD ./buildall.sh
