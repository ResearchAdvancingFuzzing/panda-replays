
# run.py yamlfile

import sys
import os
import shutil
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

# copy dir should not exist
assert(not (os.path.exists(y["copydir"]))), f"You need to rm -rf {y['copydir']}"
       
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
       

@blocking
def record_cmds():
    # create copydir
    #os.makedirs(y["copydir"])

    # copy inputfile and installdir
    panda.revert_sync(y["snapshot"])
    panda.copy_to_guest(y["copydir"])
    # TODO: what command should we run in the guest?
    cmd = "ls"

    panda.type_serial_cmd(cmd) # Type command, don't push enter

    print(f"Beginning recording: {y['replayname']}")
    panda.run_monitor_cmd("begin_record {}".format(y["replayname"])) # Begin recording
    result = panda.finish_serial_cmd() # Push enter

    panda.run_monitor_cmd("end_record")
    print(f"Ran command `{cmd}`")
    print(f"Result: {result}")
    panda.end_analysis()

# inputfile is copied as part of copytree
#shutil.copy(y["inputfile"], y["copydir"])
shutil.copytree(y["installdir"], y["copydir"])

panda = Panda(generic="i386", qcow=qcf)
panda.queue_async(record_cmds)
panda.run()
