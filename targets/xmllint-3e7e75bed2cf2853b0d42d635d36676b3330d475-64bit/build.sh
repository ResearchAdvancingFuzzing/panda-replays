#!/bin/bash 
set -e 


docker build --no-cache -t panda-xmllint-3e7e75bed2cf2853b0d42d635d36676b3330d475-64bit .
rm -rf install
mkdir install
docker run -v `pwd`/install:/install panda-xmllint-3e7e75bed2cf2853b0d42d635d36676b3330d475-64bit cp -r libxml2 install
# make installed version NOT root:root
# but owned by current user and has whatever group that person has
sudo chown -R $USER:"`id -g -n`" install


QCOW_URL=`grep qcow yamlfile | awk '{print $2}'`
#echo QCOW_URL $QCOW_URL

QCOW_BASE=`basename $QCOW_URL`
#echo QCOW_BASE $QCOW_BASE

QCOW_FILE="../../qcows/$QCOW_BASE"

if test -f "$QCOW_FILE"; then
    echo "Qcow present: $QCOW_BASE"
else
    echo "Obtaining qcow: $QCOW_BASE"
    wget -O $QCOW_FILE $QCOW_URL
fi

   
