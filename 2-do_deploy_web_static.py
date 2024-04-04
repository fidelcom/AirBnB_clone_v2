#!/usr/bin/python3
"""This is a fabric script that distributes an archive to your web servers,
using the function do_deploy"""
from fabric.api import *
import os


env.hosts = ['100.26.168.29', '54.173.39.101']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Distributes an archive to web servers."""

    if not os.path.exists(archive_path):
        return False

    try:
        for host in env.hosts:
            put(archive_path, "/tmp/")

        filename os.path.basename(archive_path)
        filename_without_ext = os.path.splitext(filename)[0]

        release_dir = '/data/web_static/releases/{filename_without_ext}'
        run('sudo mkdir -p {}'.format(release_dir))
        run('sudo tar -xvf /tmp/{} -C {}'.format(filename, release_dir))
        run('sudo rm /tmp/{}'.format(filename))
        run('sudo rm -f /data/web_static/current')
        run('sudo ln -sf {} /data/web_static/current'.format(release_dir))

        return True

    except Exception as e:
        return False
