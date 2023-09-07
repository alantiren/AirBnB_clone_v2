#!/usr/bin/python3
# Fabric script that generates a .tgz archive from the contents of the
# web_static folder of your AirBnB Clone repo
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the web_static folder
    """

    if not os.path.exists("versions"):
        os.makedirs("versions")

    archive_name = "web_static_{}.tgz".format(
        now.strftime("%Y%m%d%H%M%S"))

    archive_command = "tar -cvzf versions/{} web_static".format(archive_name)

    result = local(archive_command)

    if result.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None

if __name__ == "__main__":
    do_pack()
