#!/bin/bash

P=`pwd`
PR=`realpath $P/../..`

echo docker run -v $PR:/panda-replays panda bash -c "cd /panda-replays/targets/xmllint-3e7e75bed2cf2853b0d42d635d36676b3330d475-64bit; python3.6 ./run.py ./yamlfile $1"
docker run -v $PR:/panda-replays panda bash -c "cd /panda-replays/targets/xmllint-3e7e75bed2cf2853b0d42d635d36676b3330d475-64bit; python3.6 ./run.py ./yamlfile $1"
