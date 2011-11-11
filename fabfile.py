import os
import time
import datetime
import fabric
from random import Random
from getpass import getpass
from fabric.api import *
from fabric.operations import prompt
from fabric.contrib import django


env.root_dir = os.path.abspath(os.path.dirname(__file__))
env.unit = os.path.split(env.root_dir)[1]
django.project('apps')
from django.conf import settings

env.path = "/home/journal/webapps/%(unit)s" % env
env.source = "git@bitbucket.com:tylerball/%(unit)s.git" % env
env.source_http = "https://tylerball@bitbucket.org/tylerball/%(unit)s.git" % env
env.django_root = os.path.join(env.root_dir, 'apps/')

env.hosts=['journal@queensjournal.ca']
env.media='webapps/media'
env.activate='source webapps/journal/bin/activate'
supervisor_task = 'journal'

local_dumps = os.path.join(env.root_dir, 'dumps/')

env.pip_requirements = "requirements/common.txt"
env.pip_requirements_prod = "requirements/prod.txt"

rng = Random()
r_seed = "1234567890qwertyuiopasdfghjklzxcvbnm"
env.secret_key = ""
for i in range(30):
    env.secret_key += rng.choice(r_seed)

def echo(msg):
    local('echo %s' % msg)

def local_env(cmd):
    local('source %s/bin/activate && %s' % (env.root_dir, cmd))

def setup_localsettings():
    with hide('running'):
        env.password = getpass("Enter a password for your database")
        with lcd(env.django_root):
            echo("Creating settings_local.py")
            local("sed 's/<projectname>/%s/g' settings_local.py.ex > settings_local.py" % env.unit)
            local("sed 's/<password>/%s/g' settings_local.py > settings_local.py.1" % env.password)
            local("sed 's/<secretkey>/%s/g' settings_local.py.1 > settings_local.py")
            local("rm settings_local.py.1")

def setup_localdb():
    with hide('running'):
        local("createuser --no-createrole --no-superuser --createdb --pwprompt %s" % env.unit)
        local("createdb %(unit)s --owner %(unit)s" % env)
        local("echo '*:*:%(unit)s:%(unit)s:%(password)s' >> ~/.pgpass" % env)
        local("chmod 0600 ~/.pgpass")

def setup_localreqs():
    with hide('running'):
        echo('updating requirements')
        with lcd(env.root_dir):
            local('pip install -r %s' % env.pip_requirements)
            local('git submodule sync')
            local('git submodule init')
            local('git submodule update')

def test_all():
    with lcd(env.django_root):
        local('./manage.py test')

def setup_local():
    setup_localreqs()
    setup_localsettings()
    setup_localdb()
    test_all()

def virtualenv(command):
    with cd(env.path):
        run(env.activate + ' && ' + command)

def restart():
    sudo('supervisorctl restart %s' % supervisor_task)

def update():
    virtualenv('git pull origin')
    virtualenv('pip install -r %(pip_requirements)s' % env)
    virtualenv('git submodule sync')
    virtualenv('git submodule init')
    virtualenv('git submodule update')

def pulldump():
    # Make sure theres a dumps dir
    try:
        lcd(local_dumps)
    except:
        local('mkdir %s/dumps' % env.path)

    # Kill off any dumps older than a month
    with hide("running"):
        output = run('ls %s/dumps' % env.path)
        files = output.split()
        ctimes = {}
        for f in files:
            ctimes[f] = run("python <<< 'import os; print os.path.getctime(\"%s/dumps/%s\")'" % \
                (env.path, f))

    for f in ctimes.keys():
        if float(ctimes[f]) < (time.time() - (30 * 24 * 60 * 60)):
            run('rm %s/dumps/%s' % (env.path, f))

    try:
        with lcd(local_dumps):
            local('tar -xvf {}/journal-`date +%F`.tar.gz'.format(local_dumps))
    except:
        try:
            local('scp {}:{}/dumps/journal-`date +%F`.tar.gz {}'.format(env.host_string, env.path, local_dumps))
        except:
            run('pg_dump -h localhost -U postgres --clean --no-owner --no-privileges {0[unit]} \
            > {0[path]}/dumps/journal-`date +%F`.sql'.format(env))
            with cd('%s/dumps' % env.path):
                run('tar -czf journal-`date +%F`.tar.gz journal-`date +%F`.sql')
            local('scp {}:{}/dumps/journal-`date +%F`.tar.gz {}'.format(env.host_string, env.path, local_dumps))
            run('rm %(path)s/dumps/%(unit)s-`date +%F`.sql' % env)
    with lcd(env.django_root):
        local_env('./manage.py dbshell < ../dumps/journal-`date +%F`.sql')

def pullmedia():
    local('rsync -autvz --progress --exclude="cache/" --exclude="photo_cache/" \
        %(host_string)s:%(media)s/* ' % env + settings.MEDIA_ROOT)
