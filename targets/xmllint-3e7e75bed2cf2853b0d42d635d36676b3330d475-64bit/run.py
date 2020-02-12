
# run.py yamlfile

import sys
import os
from stat import *
import glob
from os.path import basename
import subprocess as sp
import yaml

from panda import Panda, blocking

y = yaml.load(open(sys.argv[1]), Loader=yaml.FullLoader)


inputfile = sys.argv[2]


assert "installdir" in y
assert "qcow" in y
assert "snapshot" in y
assert "copydir" in y

# naming?
qcowfile = basename(y["qcow"])


# input file should exist
assert(os.path.exists(inputfile))
assert(os.path.isfile(inputfile))

print("installdir: [%s]" % y["installdir"])

# install dir should exist
# input file should exist
assert(os.path.exists(y["installdir"]))
assert(os.path.isdir(y["installdir"]))

# qcowfile should exist
qcf = "../../qcows/" + qcowfile
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
shutil.copy(inputfile, y["copydir"])
shutil.copytree(y["installdir"], y["copydir"]+"/install")

# we'll write replay files here
# but bc of -v magic that will be the right host location
replayname = "/replay/" + basename(inputfile) + "-panda"
print ("replay name = [%s]" % replayname)

@blocking
def record_cmds():

    panda.revert_sync(y["snapshot"])
    panda.copy_to_guest(y["copydir"], iso_name="foo.iso")

    cmd = "cd copydir/install/libxml2/.libs && ./xmllint ~/copydir/"+basename(inputfile)
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



with open ("/replay/run.log", "w") as ml:
    for fn in glob.glob("%s-rr-*" % replayname):
        ml.write ("chmod %s\n" % fn)
        os.chmod(fn, S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IROTH)




