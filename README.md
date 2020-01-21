# panda-replays
Repository to house scripts enabling one to collect panda replays for various open source software projects

Running a program s.t. PANDA can create a recording is work we'd like to do once for a target.  
This repository is where we will store the domain knowledge required to harness a program.

The basic idea is that each subdirectory will contain two scripts

`build.sh` which clones and compiles the program under docker, depositing the resulting build directory in a subdirectory `install`.

`run.py` which uses pypanda to run the program and generate a replay.  This script takes a pair of parameters, the first is the path to the input file. The second is the name of the replay to create.
