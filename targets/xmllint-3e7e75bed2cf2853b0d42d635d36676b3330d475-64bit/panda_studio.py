
# run.py yamlfile

import shutil
import sys
import os
import yaml
import docker
import subprocess as sp
from os import getcwd, mkdir, rmdir
from os.path import basename, join
from shutil import rmtree
from panda import Panda, blocking
import subprocess

import argparse
parser = argparse.ArgumentParser(prog="panda_studio",description="make recordings of arbitrary programs with Docker and PANDA!")
parser.add_argument("--yaml", help="yaml file to supply all the interesting arguments")
parser.add_argument('--qcow', help="path to qcow file to use.")
parser.add_argument("--installdir", help="directory of files to move into the guest")
parser.add_argument("--replaydir", help="directory to output replay files to")
parser.add_argument("--snapshot", help="snapshot name")
parser.add_argument("--copydir", help="")
args = parser.parse_args()

if args.yaml:
    y = yaml.load(open(args.yaml), Loader=yaml.FullLoader)
else:
    y = {}



sys.exit(0)



inputfile = sys.argv[2]


assert "replaydir" in y
assert "qcow" in y
assert "snapshot" in y
assert "copydir" in y
assert "dockertag" in y
assert "dockerfile" in y

client = docker.from_env()
if not any([any([y["dockertag"] in tag for tag in image.tags]) for image in client.images.list()]):
    print("building docker image...")
    client.images.build(
        path=".", dockerfile=y["dockerfile"], tag=y["dockertag"], nocache=True, quiet=False)
else:
    print("working from previously built docker image")

# clear each time
print("creating build directory...")

rmtree(join(getcwd(), y["installdir"]),ignore_errors=True)
mkdir(y["installdir"])

if os.path.exists(y["copydir"]):
    shutil.rmtree(y["copydir"])
os.makedirs(y["copydir"])

# make the output our uid
myuid = os.geteuid()
movecmd = f"sh -c 'cp -r libxml2 install; chown -R {myuid}:{myuid} install; chmod -R 777 install;'"
client.containers.run(y["dockertag"], movecmd, volumes={join(
    getcwd(), y["installdir"]): {'bind': '/install/', 'mode': 'rw'}})

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



# copy inputfile and installdir
shutil.copy(inputfile, y["copydir"])
shutil.copytree(y["installdir"], y["copydir"]+"/install")

# we'll write replay files here
# but bc of -v magic that will be the right host location
replayname = y["replaydir"] + basename(inputfile) + "-panda"
print("replay name = [%s]" % replayname)


@blocking
def record_cmds():

    panda.revert_sync(y["snapshot"])
    panda.copy_to_guest(y["copydir"], iso_name="foo.iso")

    cmd = "cd copydir/install/libxml2/.libs && ./xmllint ~/copydir/" + \
        basename(inputfile)
    panda.type_serial_cmd(cmd)

    print(f"Beginning recording: {replayname}")
    panda.run_monitor_cmd("begin_record {}".format(
        replayname))  # Begin recording

    result = panda.finish_serial_cmd()

    panda.run_monitor_cmd("end_record")

    print(f"Ran command `{cmd}`")
    print(f"Result: {result}")

    panda.end_analysis()


panda = Panda(arch="x86_64", expect_prompt=rb"root@ubuntu:.*#",
              qcow=qcf, mem="1G", extra_args="-display none -nographic")
panda.queue_async(record_cmds)
panda.run()
