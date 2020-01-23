git clone git@github.com:panda-re/panda.git
cd panda
git checkout pypanda-dev
git submodule update --init dtc
mkdir build
cd build
../build.sh
