#!/usr/bin/python3
from fabric.api import local, put, env, run
from time import strftime
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['100.26.168.29', '54.173.39.101']


def do_pack():
    """ A script that generates archive the contents of web_static folder"""

    filename = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(filename))

        return "versions/web_static_{}.tgz".format(filename)

    except Exception as e:
        return None


def do_deploy(archive_path):
    """Deploy web files to server"""
    try:
        if not (path.exists(archive_path)):
            return False

        put(archive_path, '/tmp/')
        filename = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'
            .format(filename))

        run("sudo tar -xzf /tmp/web_static_{}.tgz -C"
            "/data/web_static/releases/web_static_{}/"
            .format(filename, filename))

        run('sudo rm /tmp/web_static_{}.tgz'.format(filename))

        run('sudo mv /data/web_static/releases/web_static_{}/web_static/*'
            '/data/web_static/releases/web_static_{}/'
            .format(filename, filename))

        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'
            .format(filename))

        run('sudo rm -rf /data/web_static/current')

        run('sudo ln -s /data/web_static/releases/web_static_{}/'
            '/data/web_static/current'.format(filename))
    except Exception:
        return False

    return True


def deploy():
    """
    Function Docs
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
