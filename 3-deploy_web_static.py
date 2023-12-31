#!/usr/bin/python3
# Fabric script to create and distribute an archive to web servers
from fabric.api import local, env, put, run
from datetime import datetime
from os.path import exists
from pathlib import Path

env.user = 'ubuntu'
env.hosts = ['52.3.241.14', '34.224.4.0']


def do_pack():
    """
    Generate a .tgz archive from the web_static folder
    """
    now = datetime.now()
    formatted_time = now.strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(formatted_time)

    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(archive_path))

    if result.succeeded:
        return archive_path
    else:
        return None

def do_deploy(archive_path):
    """
    Distribute an archive to web servers
    """

    if not exists(archive_path):
        return False

    try:

        put(archive_path, '/tmp/')

        filename = Path(archive_path).stem
        folder_name = "web_static_" + filename
        release_path = '/data/web_static/releases/' + folder_name
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(filename + '.tgz', release_path))

        run('rm /tmp/{}'.format(filename + '.tgz'))

        run('mv {}/web_static/* {}'.format(release_path, release_path))

        run('rm -rf {}/web_static'.format(release_path))

        current_path = '/data/web_static/current'
        if run('test -e {}'.format(current_path)).succeeded:
            run('rm {}'.format(current_path))

        run('ln -s {} {}'.format(release_path, current_path))

        print("New version deployed!")
        return True
    except Exception as e:
        return False

def deploy():
    """
    Deploy the web_static content to web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

if __name__ == "__main__":
    deploy()
