from fabric.api import *

env.hosts=['3781lanru0j@queensjournal.ca']
env.directory='/home/3781lanru0j/webapps/journal'
env.activate='source /home/3781lanru0j/webapps/journal/bin/activate'

def virtualenv(command):
    with cd(env.directory):
        run(env.activate + '&&' + command)
        
def stage():
    local('git push origin master')
    local('pip freeze > requirements.txt')
    with cd(env.directory):
        run('git pull origin master')
    virtualenv('pip install -r requirements.txt')
    restart()
    
def restart():
    virtualenv('%s/apache2/bin/stop' % (env.directory))
    virtualenv('%s/apache2/bin/start' % (env.directory))
    
def update():
    local('git push origin master')
    with cd(env.directory):
        run('git pull origin master')
    restart()