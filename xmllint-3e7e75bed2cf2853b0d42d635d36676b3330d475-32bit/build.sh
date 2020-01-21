docker build --no-cache -t panda-xmllint .
mkdir install
docker run -v `pwd`/install:/install panda-xmllint cp -r libxml2 install
sudo chown -R $USER:$USER install/

