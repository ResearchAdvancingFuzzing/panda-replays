
# run.py yamlfile

import sys
import os
from os.path import basename
import subprocess as sp

from panda import Panda, blocking


import yaml

y = yaml.load(open(sys.argv[1]), Loader=yaml.FullLoader)

assert "inputfile" in y
assert "installdir" in y
assert "replaydir" in y
assert "qcow" in y
assert "snapshot" in y
assert "copydir" in y

# naming?
qcowfile = basename(y["qcow"])


# input file should exist
assert(os.path.exists(y["inputfile"]))
assert(os.path.isfile(y["inputfile"]))

# install dir should exist
# input file should exist
assert(os.path.exists(y["installdir"]))
assert(os.path.isdir(y["installdir"]))

# qcowfile should exist
qcf = "../qcows/" + qcowfile
if not os.path.exists(qcf):
    if not os.path.exists("../qcows"):
        os.makedirs("../qcows")
    sp.check_call(["wget", y["qcow"], "-O", qcf])


assert(os.path.isfile(qcf))


import shutil

if os.path.exists(y["copydir"]):
    shutil.rmtree(y["copydir"])
os.makedirs(y["copydir"])

# copy inputfile and installdir
shutil.copy(y["inputfile"], y["copydir"])
shutil.copytree(y["installdir"], y["copydir"]+"/install")

replayname = y["replaydir"] + "/" + basename(y["inputfile"]) + "-panda"
print ("replay name = [%s]" % replayname)

@blocking
def record_cmds():

    print("here1")
    panda.revert_sync(y["snapshot"])
    panda.copy_to_guest(y["copydir"], iso_name="foo.iso")

    cmd = "cd copydir/install/libxml2/.libs && ./xmllint ~/copydir/"+basename(y["inputfile"])
    panda.type_serial_cmd(cmd)

    print(f"Beginning recording: {replayname}")
    panda.run_monitor_cmd("begin_record {}".format(replayname)) # Begin recording

    result = panda.finish_serial_cmd() 

    panda.run_monitor_cmd("end_record")

    print(f"Ran command `{cmd}`")
    print(f"Result: {result}")

    panda.end_analysis()

 

panda = Panda(arch="x86_64", expect_prompt=rb"root@ubuntu:.*#", qcow=qcf, mem="1G", extra_args="-display none -nographic")
panda.queue_async(record_cmds)
panda.run()

