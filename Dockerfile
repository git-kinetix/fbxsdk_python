FROM quay.io/pypa/manylinux2014_x86_64

ARG pass

VOLUME /build

WORKDIR /build

CMD ./buildall.sh
