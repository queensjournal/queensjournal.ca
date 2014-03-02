import os
import subprocess
from random import Random
from fabric.api import local, cd, run, env, lcd, sudo, prefix
from fabric.operations import get
from fabric.contrib import django


django.project('journal')
from django.conf import settings

# Variable setup
env.project_root = settings.PROJECT_ROOT
env.project_name = settings.PROJECT_NAME

env.path = "/home/journal/%(project_name)s" % env
env.django_root = os.path.join(env.project_root, 'apps/')

env.hosts = ['journal@queensjournal.ca']
env.media = env.path + '/media/'

local_dumps = os.path.join(env.project_root, 'dumps/')

env.pip_requirements = "requirements.txt"


# helper functions
def generate_random():
    rng = Random()
    r_seed = "1234567890qwertyuiopasdfghjklzxcvbnm"
    env.secret_key = ""
    for i in range(30):
        env.secret_key += rng.choice(r_seed)


def echo(msg):
    local('echo %s' % msg)


def local_env(cmd):
    local('source %s/bin/activate && %s' % (env.root_dir, cmd))


def remote_env(command):
    with cd(env.path):
        with prefix('source bin/activate'):
            run(command)


def remote_run(command):
    with cd(env.path):
        run(command)


def restart():
    sudo('supervisorctl restart %s' % env.project_name)


def update_requirements():
    '''
    Update python requirements on the server
    '''
    remote_env('pip install -r %(pip_requirements)s' % env)


def collectstatic():
    remote_env('python apps/manage.py collectstatic -c --noinput')


def deploy(tag=None):
    '''
    Update the remote server with the latest git tag
    '''
    remote_run('git fetch origin --tags')
    if not tag:
        tag = subprocess.check_output('git describe --abbrev=0 --tags',
            shell=True).rstrip()
    remote_run('git checkout %s' % tag)


def deploy_latest():
    remote_run('git checkout master')
    remote_run('git pull origin master')


def deploy_sha(sha=None):
    '''
    Update the remote server with a specified ref or latest master
    '''
    remote_run('git fetch master')
    remote_run('git checkout master')


def make_dump(db):
    dump_loc = os.path.join(env.path, 'devdata/dump.sql')
    remote_run('mkdir -p devdata')
    remote_run('pg_dump -v -h localhost -U postgres --clean --no-owner --no-privileges \
        --format=custom {db} -f {dump_loc}'.format(db=db, dump_loc=dump_loc))


def get_dump():
    get(os.path.join(env.path, 'devdata/dump.sql'))

def get_media():
    get(os.path.join(env.path, 'media/'), settings.MEDIA_ROOT)
