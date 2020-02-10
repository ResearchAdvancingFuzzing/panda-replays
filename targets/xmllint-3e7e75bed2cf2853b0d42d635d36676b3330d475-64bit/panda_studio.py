
# run.py yamlfile

import shutil
import sys
import os
import yaml
import docker
import subprocess as sp
from os import getcwd, mkdir, rmdir
from os.path import basename, join, realpath, dirname
from shutil import rmtree
from panda import Panda, blocking
import subprocess

import argparse

fpath = dirname(realpath(__file__))

parser = argparse.ArgumentParser(prog="panda_studio",description="Make recordings of arbitrary programs with Docker and PANDA!",add_help=True)
parser.add_argument("--yaml", help="Yaml file to supply all the interesting arguments",default=None)
parser.add_argument('--qcow', help="Path to qcow file to use.",default="http://panda-re.mit.edu/qcows/linux/ubuntu/1804/bionic-server-cloudimg-amd64.qcow2")
parser.add_argument("--installdir", help="Directory of files to move into the guest. Default is local to script.", default=join(fpath,"install"))
parser.add_argument("--replaydir", help="Directory to output replay files to. Default is script directory.",default=fpath)
parser.add_argument("--snapshot", help="Name of snapshot to restore",default="root")
parser.add_argument("--copydir", help="Path to copy items to. Default is folder local to script.",default=join(fpath,"copydir"))
parser.add_argument("--dockerfile", help="Path to docker file. Default is example in directory.", default=join(fpath,"Dockerfile"))
parser.add_argument("--dockertag", help="Tag on docker container. Default is example.", default="panda-xmllint")
parser.add_argument("--inputfile")
args = parser.parse_args()

if args.yaml:
    y = yaml.load(open(args.yaml), Loader=yaml.FullLoader)
else:
    y = vars(args)


#inputfile = sys.argv[2]
inputfile = y["inputfile"]
assert "inputfile" in y and not y["inputfile"] is None 
assert "replaydir"in y and not y["replaydir"] is None 
assert "qcow" in y and not y["qcow"] is None 
assert "snapshot" in y and not y["snapshot"] is None 
assert "copydir" in y and not y["copydir"] is None 
assert "dockertag" in y and not y["dockertag"] is None 
assert "dockerfile" in y and not y["dockerfile"] is None 

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