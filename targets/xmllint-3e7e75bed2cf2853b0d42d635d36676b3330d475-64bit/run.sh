#!/bin/bash

HERE=`pwd`

# directory in which run.sh lives
P=`dirname $0`

# panda-replay dir
PRD=`realpath $P/../..`

# the input file
I=$1
IB=`basename $I`

# input dir
ID1=`dirname $I`
ID=`realpath $ID1`

# directory (on host) where replay should be deposited
# which is wherever run.sh is run from
RD=$HERE

#echo P = $P
#echo PRD = $PRD
#echo I = $I
#echo IB = $IB
#echo ID = $ID
#echo RD = $RD


echo docker run -v $PRD:/panda-replays -v $ID:/input -v $RD:/replay panda bash -c "cd /panda-replays/targets/xmllint-3e7e75bed2cf2853b0d42d635d36676b3330d475-64bit; python3.6 ./run.py ./yamlfile /input/$IB"
docker run -v $PRD:/panda-replays -v $ID:/input -v $RD:/replay panda bash -c "cd /panda-replays/targets/xmllint-3e7e75bed2cf2853b0d42d635d36676b3330d475-64bit; python3.6 ./run.py ./yamlfile /input/$IB"

