#!/bin/bash
set -e

rm Dockerfile_18_04* || true

#wget https://raw.githubusercontent.com/panda-re/panda/spitfire/panda/docker/Dockerfile_18_04
wget https://raw.githubusercontent.com/panda-re/panda/master/panda/docker/Dockerfile_18_04
sed '/^WORKDIR \"\/panda\/panda\/pypanda\"/i RUN pip install pyyaml' Dockerfile_18_04 > Dockerfile_18_04.patched
#cd panda

docker build -f ./Dockerfile_18_04.patched -t panda .

mkdir qcows
