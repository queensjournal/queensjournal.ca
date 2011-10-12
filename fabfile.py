from fabric.api import *

env.hosts=['journal@queensjournal.ca']
env.directory='webapps/journal'
env.media='webapps/media'
env.activate='source webapps/journal/bin/activate'
supervisor_task = 'journal'

local_django = '~/Sites/queensjournal.ca/apps'
local_dumps = '~/Sites/queensjournal.ca/dumps'

def local_env(command):
    local('source %s/../bin/activate && %s' % (local_django, command))

def virtualenv(command):
    with cd(env.directory):
        run(env.activate + ' && ' + command)
    
def restart():
    sudo('supervisorctl restart %s' % supervisor_task)
        
def stage():
    local('git push origin master')
    local('pip freeze > requirements.txt')
    with cd(env.directory):
        run('git pull origin master')
    virtualenv('pip install -r requirements.txt')
    restart()
    
def update():
    local('git push origin master')
    with cd(env.directory):
        run('git pull origin master')
    restart()

def pulldump():
    with cd(local_dumps) and settings(warn_only=True):
        # Kill off any other dumps made today
        try:
            run('rm journal-`date +%F`*')
            run('pg_dump -h localhost -U postgres --clean --no-owner --no-privileges journal > {}/dumps/journal-`date +%F`.sql'.format(env.directory))
            with cd('%s/dumps' % env.directory):
                run('tar -czf journal-`date +%F`.tar.gz journal-`date +%F`.sql')
            local('scp {}:{}/dumps/journal-`date +%F`.tar.gz {}/'.format(env.host_string, env.directory, local_dumps))
        except:
            local('scp {}:{}/dumps/journal-`date +%F`.tar.gz {}/'.format(env.host_string, env.directory, local_dumps))
        local('tar -xzvf {}/journal-`date +%F`.tar.gz'.format(local_dumps))
    local_env('./manage.py dbshell < ../dumps/journal-`date +%F`.sql')

def pullmedia():
    with cd(env.media):
        run('tar -czv --exclude="cache/" --exclude="photo_cache/" -f media-`date +%F`.tar.gz .')
    local('scp {}:{}/media-`date +%F`.tar.gz {}/'.format(env.host_string, env.media, local_dumps))
