#!/usr/bin/python3
"""
Fabric script to delete out-of-date archives
"""

from fabric.api import local, env, run
from os.path import exists, join
from datetime import datetime
from pathlib import Path

# Define the remote user and hosts
env.user = 'ubuntu'
env.hosts = ['<IP web-01>', '<IP web-02>']

def do_clean(number=0):
    """
    Delete out-of-date archives
    """
    if int(number) < 0:
        return

    try:
        number = int(number)
        keep = number if number >= 2 else 1

        # Clean the local versions folder
        local("ls -t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}".format(keep + 1))

        # Clean the remote versions folder on both servers
        releases_path = '/data/web_static/releases'
        releases = run("ls -t {}".format(releases_path)).split()
        if len(releases) > keep:
            for release in releases[keep:]:
                run("rm -rf {}/{}".format(releases_path, release))

        print("Done.")
    except Exception as e:
        pass

if __name__ == "__main__":
    do_clean()
