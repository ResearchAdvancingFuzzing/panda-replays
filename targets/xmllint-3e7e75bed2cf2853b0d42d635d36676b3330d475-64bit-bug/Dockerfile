FROM amd64/ubuntu:18.04


#FROM i386/debian:stretch
#RUN echo deb http://archive.debian.org/debian wheezy-backports main >> /etc/apt/sources.list

RUN apt-get update



RUN apt-get -y install git build-essential libtool autoconf pkg-config


RUN git clone https://gitlab.gnome.org/GNOME/libxml2.git

WORKDIR libxml2
RUN git checkout 3e7e75bed2cf2853b0d42d635d36676b3330d475
COPY ./parser.patch ./parser.patch
RUN patch -u parser.c -i parser.patch
RUN ./autogen.sh
RUN ./configure && make

WORKDIR /
