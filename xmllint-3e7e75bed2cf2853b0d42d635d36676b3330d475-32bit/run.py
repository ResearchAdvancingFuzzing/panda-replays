
# run.py yamlfile

import sys
import os
import subprocess as sp

# walk up the path to find 'panda' and add that to python path 
# at most 10 levels up?  
p = os.path.abspath(__file__)
foundit=False
for i in range(10):
    if foundit: 
        break
    (hd, tl) = os.path.split(p)
    for x in os.listdir(hd):
        if x == "panda":
            pypanda = os.path.join(hd, x) + "/panda/pypanda"
            print("adding path " + pypanda)
            sys.path.append(pypanda)
            foundit = True
            break
    p = hd

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
assert(not (os.path.exists(y["copydir"])))
       
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
def record_cmds(panda):

    # create copydir
    os.makedirs(y["copydir"])

    # copy inputfile and installdir
    shutil.copy(y["inputfile"], y["copydir"])
    shutil.copytree(y["installdir"], y["copydir"])

    panda_revert_sync(y["snapshot"])
    panda.copy_to_guest(copy_dir, iso_name)
    panda.type_serial_cmd("ls")

    


panda = Panda(generic="i386", qcow=qcf)
panda.queue_async(record_cmds)

    
    
