
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

    panda.revert_sync(y["snapshot"])
    panda.copy_to_guest(y["copydir"], iso_name="foo.iso")



    # this works (in the sense that the command executes and we get result back
#    panda.type_serial_cmd("cd /bin")
#    result = panda.finish_serial_cmd() 
#    print("serial result = [%s]" % result)

    # this doesn't work?  Hangs forever.  :<
    # Note: even if I delete code prior to this which does ls ..
    # this one still doesn't work.
#    panda.type_serial_cmd("cd copydir/install/libxml2/.libs && ./xmllint ~/slashdot.xml")
    panda.type_serial_cmd("ls")
    result = panda.finish_serial_cmd() 
    print("serial result = [%s]" % result)

    # This doesn't work either? 
    # panda.type_serial_cmd("cd copydir/install/libxml2")
    # result = panda.finish_serial_cmd() 
    # print("serial result = [%s]" % result)
    # panda.type_serial_cmd("xmllint ~/slashdot.xml")
    # result = panda.finish_serial_cmd() 
    # print("serial result = [%s]" % result)

    panda.end_analysis()

 

# panda = Panda(generic="i386", qcow=qcf)
panda = Panda(arch="x86_64", expect_prompt=rb"root@ubuntu:~#", qcow=qcf, mem="1G", extra_args="-display none")
panda.queue_async(record_cmds)
panda.run()

