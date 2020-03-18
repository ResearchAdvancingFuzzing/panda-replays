#!/bin/bash
set -e

rm Dockerfile_18_04*

#wget https://raw.githubusercontent.com/panda-re/panda/spitfire/panda/docker/Dockerfile_18_04
wget https://raw.githubusercontent.com/panda-re/panda/master/panda/docker/Dockerfile_18_04
sed '/^WORKDIR \"\/panda\/panda\/pypanda\"/i RUN pip install pyyaml'
#cd panda

docker build -f ./Dockerfile_18_04 -t panda .

mkdir qcows
