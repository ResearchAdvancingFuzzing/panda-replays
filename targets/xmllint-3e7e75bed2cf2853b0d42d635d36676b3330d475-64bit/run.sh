#!/bin/bash

P=`dirname $0`
PRD=`realpath $P/../..`

I=$1
IB=`basename $I`
ID=`dirname $I`

docker run -v $PRD:/panda-replays -v $ID:/input panda bash  \
       -c "cd /panda-replays/targets/xmllint-3e7e75bed2cf2853b0d42d635d36676b3330d475-64bit; python3.6 ./run.py ./yamlfile /input/$IB"
