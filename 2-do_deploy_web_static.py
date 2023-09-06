#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""

from fabric.api import local, env, put, run
from datetime import datetime
import os

# Define the remote user and hosts
env.user = 'ubuntu'
env.hosts = ['<IP web-01>', '<IP web-02>']

def do_deploy(archive_path):
    """
    Distribute an archive to web servers
    """

    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ on the server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/
        filename = os.path.basename(archive_path)
        folder_name = filename.split('.')[0]
        release_path = '/data/web_static/releases/' + folder_name
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(filename, release_path))

        # Delete the uploaded archive from /tmp/
        run('rm /tmp/{}'.format(filename))

        # Move the contents of the extracted folder to the release path
        run('mv {}/web_static/* {}'.format(release_path, release_path))

        # Remove the empty web_static folder
        run('rm -rf {}/web_static'.format(release_path))

        # Delete the current symbolic link if it exists
        current_path = '/data/web_static/current'
        if run('test -e {}'.format(current_path)).succeeded:
            run('rm {}'.format(current_path))

        # Create a new symbolic link
        run('ln -s {} {}'.format(release_path, current_path))

        print("New version deployed!")
        return True
    except Exception as e:
        return False

if __name__ == "__main__":
    do_deploy("<path_to_your_archive>")
