import os
import subprocess
from random import Random
from fabric.api import local, cd, run, env, lcd, sudo, prefix
from fabric.contrib import django


django.project('apps')
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


#def setup_localsettings():
    #with hide('running'):
        #env.password = getpass("Enter a password for your database")
        #with lcd(env.django_root):
            #echo("Creating settings_local.py")
            #local("sed 's/<projectname>/%s/g' settings_local.py.ex > settings_local.py" % env.unit)
            #local("sed 's/<password>/%s/g' settings_local.py > settings_local.py.1" % env.password)
            #local("sed 's/<secretkey>/%s/g' settings_local.py.1 > settings_local.py")
            #local("rm settings_local.py.1")


#def setup_localdb():
    #with hide('running'):
        #local("createuser --no-createrole --no-superuser --createdb --pwprompt %s" % env.unit)
        #local("createdb %(unit)s --owner %(unit)s" % env)
        #local("echo '*:*:%(unit)s:%(unit)s:%(password)s' >> ~/.pgpass" % env)
        #local("chmod 0600 ~/.pgpass")


#def setup_localreqs():
    #with hide('running'):
        #echo('updating requirements')
        #with lcd(env.root_dir):
            #local('pip install -r %s' % env.pip_requirements)
            #local('git submodule sync')
            #local('git submodule init')
            #local('git submodule update')


def test_all():
    '''
    Run unit tests.
    '''
    with lcd(env.django_root):
        local('./manage.py test')


#def setup_local():
    #setup_localreqs()
    #setup_localsettings()
    #setup_localdb()
    #test_all()


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


#def pulldump():
    ## Make sure theres a dumps dir
    #try:
        #lcd(local_dumps)
    #except:
        #local('mkdir %s/dumps' % env.path)

    ## Kill off any dumps older than a month
    #with hide("running"):
        #output = run('ls %s/dumps' % env.path)
        #files = output.split()
        #ctimes = {}
        #for f in files:
            #ctimes[f] = run("python <<< 'import os; print os.path.getctime(\"%s/dumps/%s\")'" % \
                #(env.path, f))

    #for f in ctimes.keys():
        #if float(ctimes[f]) < (time.time() - (30 * 24 * 60 * 60)):
            #run('rm %s/dumps/%s' % (env.path, f))

    #try:
        #with lcd(local_dumps):
            #local('tar -xvf {}/journal-`date +%F`.tar.gz'.format(local_dumps))
    #except:
        #try:
            #local('scp {}:{}/dumps/journal-`date +%F`.tar.gz {}'.format(env.host_string, env.path, local_dumps))
        #except:
            #run('pg_dump -h localhost -U postgres --clean --no-owner --no-privileges {0[unit]} \
            #> {0[path]}/dumps/journal-`date +%F`.sql'.format(env))
            #with cd('%s/dumps' % env.path):
                #run('tar -czf journal-`date +%F`.tar.gz journal-`date +%F`.sql')
            #local('scp {}:{}/dumps/journal-`date +%F`.tar.gz {}'.format(env.host_string, env.path, local_dumps))
            #run('rm {}/dumps/{}-`date +%F`.sql'.format(env.path, env.unit))
    #with lcd(env.django_root):
        ##local('dropdb ' + settings.DATABASES['default']['NAME'])
        ##local('createdb %s --owner %s' % (settings.DATABASES['default']['NAME'], \
            ##settings.DATABASES['default']['USER']))
        #local_env('./manage.py dbshell < ../dumps/journal-`date +%F`.sql')


#def pullmedia():
    #local('rsync -autvz --progress --exclude="cache/" --exclude="photo_cache/" \
        #%(host_string)s:%(media)s/* ' % env + settings.MEDIA_ROOT)
