# panda-replays

This is a repository for scripts enabling one to create panda replays
for various open source software projects.

Getting to where one can run a program such that PANDA can create a
recording of that run is tricky. This is because it means creating the
version of the program that can run on guest PANDA likes, getting all
the necessary code and config files onto that guest, and finally,
issuing commands on the guest flanked by something like `begin_record`
and `end_record`. The work required to make all of that happend is
something we'd like to do once for a target and then make it generally
available to anyone for research. This repository is where we will
store the domain knowledge (in the form of scripts automating the
process) required to build and harness a program for analysis.

## Preliminaries

You'll have to build the panda docker container, which means running
the `build.sh` in this top-level directory.

  cd panda-replays
  ./build.sh

If that works you will see a lot of stuff in your terminal window, ending with

```
...
Successfully built pycparser PyYAML
Installing collected packages: pycparser, cffi, colorama, protobuf, PyYAML, pyaml
Successfully installed PyYAML-5.3 cffi-1.13.2 colorama-0.4.3 protobuf-3.11.3 pyaml-19.12.0 pycparser-2.19
Removing intermediate container 3a95304110a8
 ---> 6f41ee982bc8
 Successfully built 6f41ee982bc8
 Successfully tagged panda:latest
% 
```


## Organization

There are a number of subdirectories in `panda-replays`, each of which
represents the harnessing of an open source target program. Each
should be organized such that there exist at least a `build.sh`,
`run.sh` script, and a `yamlfile`.

1. `build.sh` script compiles the target program so that it can run on
an existing linux guest for PANDA.

2. `run.sh` script does everything from getting the compiled target
program into a booted PANDA guest to running that program against an
input specified in the yamlfile, and turning on recording before and
turning off after the program has run.  Note that `run.sh` ideally
does everything using PANDA's python interface, and thus the real
dirty work might be done by a `run.py` script.

3. `yamlfile` contains important parameters including where to put
replays and such.


## Example

As an example, consider the subdirectory
`xmllint-3e7e75bed2cf2853b0d42d635d36676b3330d475-64bit` which
contains scripts for panda-harnessing aparticular version of xmllint
(and the library it requires), You should be able to do the following
to create a recording.

  cd xmllint-3e7e75bed2cf2853b0d42d635d36676b3330d475-64bit
  ./build.sh
  ./run.sh


1. Enter the targInside that target directory there should be a `build.sh` script which somehow
obtains and compiles the version of the software and "installs" it in
the subdirectory `xmllint-3e7e75bed2cf2853b0d42d635d36676b3330d475-64bit/install`.
In that case, we use Docker to compile for a particular 

The basic idea is that each subdirectory will contain two scripts

`build.sh` which clones and compiles the program under docker, depositing the resulting build directory in a subdirectory `install`.

`run.sh` which uses pypanda to run the program and generate a replay.  This script takes a pair of parameters, the first is the path to the input file. The second is the name of the replay to create.
