from fabric.api import *

env.hosts=['3781lanru0j@queensjournal.ca']
root='/home/3781lanru0j/webapps/journal'

def deploy():
    local('git push origin master')
    with cd(root):
        run('git pull origin master')
        run('source bin/activate; pip install -r requirements.txt')
    restart()
    
def restart():
    run('%s/apache2/bin/restart' % (root))