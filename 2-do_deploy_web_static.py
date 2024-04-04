#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import *
from datetime import datetime
from os import path


env.hosts = ['100.26.168.29', '54.173.39.101']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


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
