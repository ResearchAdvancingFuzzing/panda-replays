# panda-replays

This is a repository for harnessing open source programs such that one
can use PANDA to analyze them. In particular, it will house scripts
enabling one to create PANDA replays for those program.

*NOTE*: For more information on PANDA (the Platform for Architecture-Neutral
 Dyanmic Analysis), please go to the [github site]
 (http://https://github.com/panda-re/panda).


Getting to where one can run a program such that PANDA can create a
recording of that run on an arbitrary input is tricky business. This
is because it entails all of the following.

* Creating a `qcow` guest version of an OS that PANDA likes, i.e.,
for which operating system introspection, etc are in place.
* Creating a version of the program that can run on that guest.
* Getting all the necessary code, config, and input files onto that guest.
* Orchestrating all commands or actions on the guest in the right directories
and in the right order such that the program runs on an arbitrary input.
* The run of the program also has to be bookended, temporally, by issuing
`begin_record` and `end_record` to actually create the recording.

The work required to make all of that happen is something we'd like to
do once for a target and then make it generally available to anyone
for research purposes. This repository is where we will store the domain
knowledge (in the form of scripts automating the process) required to
build and harness a particular program for analysis.


## Preliminaries

You'll have to build the PANDA docker container, which means running
the `build.sh` in this top-level directory.

```
cd panda-replays
./build.sh
```

If that works you will see a lot of stuff in your terminal window, ending with
something like the following.

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

The various `target` programs which have been harnessed and for which
there exist scripts to create recordings on inputs are in the `targets`
directory. Each subdirectory there should contain at least four files:

1. `build.sh` -- builds a version of the program
2. `run.sh` -- runs the program inside a PANDA guest, creating a recording
3. `yamlfile` -- contains parameters needed for run including where to put
replay files.
4. `inputs` -- ok this is a directory, not a file, which should contain
sample inputs (a "corpus")

There are no requirements beyond this, if you are looking to add a new
target. However, some conventions / niceties:

* You will want to "condition the `qcow` you create such that it
  contains at least one snapshot corresponding to a booted system in
  which you have logged into a working shell.

* PANDA's python interface makes a lot of this much easier. You can
  revert to a snapshot, create a snapshot, connect to and type on a
  serial port interface in order to interact with the guest
  shell. This will mean you end up with `run.sh` doing a few things
  that end up calling a python script that do all the real work of
  running the program.  Use pyPANDA unless you like pain. 
  <link to PyPANDA info?>.
 

## Example

As an example, consider the subdirectory

    xmllint-3e7e75bed2cf2853b0d42d635d36676b3330d475-64bit

which contains scripts for PANDA-harnessing a particular version of 
xmllint (and the library it requires), You should be able to do the 
following to create a recording.

    cd targets/xmllint-3e7e75bed2cf2853b0d42d635d36676b3330d475-64bit
    ./build.sh
    ./run.sh inputs/slashdot.xml

This should create a recording in the current directory, in the form of two files:

    slashdot-...
    slashdot-...

You can fiddle with the `yamlfile` to control where these files go.


## Contributing

PLEASE consider adding anything you have harnessed to this framework!
Pull requests accepted!
    

