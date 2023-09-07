#!/usr/bin/python3
# Fabric script to delete out-of-date archives
from fabric.api import local, env, run
from os.path import exists, join
from datetime import datetime
from pathlib import Path
'
env.hosts = ['52.3.241.14', '34.224.4.0']


def do_clean(number=0):
    """
    Delete out-of-date archives
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
