
# run.py yamlfile

import sys
import os
import subprocess as sp

from panda import Panda, blocking


import yaml

y = yaml.load(open(sys.argv[1]), Loader=yaml.FullLoader)

assert "inputfile" in y
assert "installdir" in y
assert "replayname" in y
assert "qcowfile" in y
assert "snapshot" in y
assert "copydir" in y


# input file should exist
assert(os.path.exists(y["inputfile"]))
assert(os.path.isfile(y["inputfile"]))

# install dir should exist
# input file should exist
assert(os.path.exists(y["installdir"]))
assert(os.path.isdir(y["installdir"]))

# qcowfile should exist
qcf = "../qcows/" + y["qcowfile"]
if not os.path.exists(qcf):
    if not os.path.exists("../qcows"):
        os.makedirs("../qcows")
    sp.check_call(["wget", "http://panda.moyix.net/~moyix/" + "wheezy_panda2.qcow2", "-O", qcf])


assert(os.path.isfile(qcf))


import shutil

if os.path.exists(y["copydir"]):
    shutil.rmtree(y["copydir"])
os.makedirs(y["copydir"])

# copy inputfile and installdir
shutil.copy(y["inputfile"], y["copydir"])
shutil.copytree(y["installdir"], y["copydir"]+"/install")

       

@blocking
def record_cmds():

    print("here1")
    panda.revert_sync(y["snapshot"])
    panda.copy_to_guest(y["copydir"], iso_name="foo.iso")

    cmd = "cd copydir/install/libxml2/.libs && ./xmllint ~/copydir/slashdot.xml"
    panda.type_serial_cmd(cmd)

    print(f"Beginning recording: {y['replayname']}")
    panda.run_monitor_cmd("begin_record {}".format(y["replayname"])) # Begin recording

    result = panda.finish_serial_cmd() 

    panda.run_monitor_cmd("end_record")

    print(f"Ran command `{cmd}`")
    print(f"Result: {result}")

    panda.end_analysis()

 

# panda = Panda(generic="i386", qcow=qcf)
# rb"root@debian-i386:.*# "
panda = Panda(arch="i386", expect_prompt=rb"ubuntu:.*#", qcow=qcf, mem="1G", extra_args="-display none")
panda.queue_async(record_cmds)
panda.run()

