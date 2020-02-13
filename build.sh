#!/bin/bash

rm Dockerfile_18_04*

#wget https://raw.githubusercontent.com/panda-re/panda/spitfire/panda/docker/Dockerfile_18_04
wget https://raw.githubusercontent.com/panda-re/panda/master/panda/docker/Dockerfile_18_04

#cd panda

docker build -f ./Dockerfile_18_04 -t panda .

cd ..
mkdir qcows
