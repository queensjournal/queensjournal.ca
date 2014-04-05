import os
import subprocess
from random import Random
from fabric.api import local, cd, run, env, sudo, prefix, task, put
from fabric.operations import get
from fabric.contrib import django


django.project('journal')
from django.conf import settings

# Variable setup
env.project_root = settings.PROJECT_ROOT
env.project_name = settings.PROJECT_NAME

env.path = "/home/journal/%(project_name)s" % env
env.django_root = os.path.join(env.project_root, 'apps/')

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


def remote_run(command, **kwargs):
    with cd(env.path):
        run(command, **kwargs)


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
        --exclude-table=django_session --format=custom {db} -f {dump_loc}'.format(db=db, dump_loc=dump_loc))


def get_dump():
    get(os.path.join(env.path, 'devdata/dump.sql'))


def get_media():
    media_folder = os.path.join(env.path, 'media/')
    dirs = run('find ' + media_folder + ' -type d -name "*2014*"').split('\r\n')
    for d in dirs:
        get(d, settings.MEDIA_ROOT)

def restore_dump():
    cmds = [
        'dropdb journal',
        'createdb journal --owner journal',
        'pg_restore -O -d journal --role=journal journal@queensjournal.ca/dump.sql',
        './manage.py syncdb',
        './manage.py migrate bento --fake',
        './manage.py migrate galleries --fake 0001',
        './manage.py migrate',
    ]
    for cmd in cmds:
        local(cmd)


@task
def install_chef():
    """
    Install chef-solo on the server
    """
    run('sudo apt-get update', pty=True)
    run('sudo apt-get -y install build-essential zlib1g-dev libssl-dev \
        libreadline6-dev libyaml-dev', pty=True)
    with cd('/tmp'):
        run('wget ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.3-p194.tar.gz')
        run('tar -xvzf ruby-1.9.3-p194.tar.gz')
        with cd('ruby-1.9.3-p194'):
            run('./configure --prefix=/usr/local')
            run('make && sudo make install')
    run('sudo gem install chef ruby-shadow --no-ri --no-rdoc')


@task
def sync_config():
    sudo('mkdir -p /etc/chef')
    local('rsync -r chef/ %s:/tmp/chef' % env.host)
    local('rsync -r tmp/librarian/cookbooks %s:/tmp/chef' % env.host)
    sudo('cp -r /tmp/chef /etc')
    sudo('rm -rf /tmp/chef')


@task
def provision(node, environment='_default'):
    """
    Run chef-solo
    """
    sync_config()

    if node:
        node_str = " -j /etc/chef/cookbooks/node_%s.json" % (node)
    else:
        node_str = ''

    with cd('/etc/chef/cookbooks'):
        sudo('chef-solo -E %s -c /etc/chef/cookbooks/solo.rb %s'
            % (environment, node_str), pty=True)
