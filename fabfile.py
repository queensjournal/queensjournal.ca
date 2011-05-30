from fabric.api import env, local, run, require, cd

fab_user='3781lanru0j'
fab_hosts=['queensjournal.ca']
root='/home/3781lanru0j/webapps/'
site='journal'

def deploy():
    local('git push origin master')
    run('cd $(root)$(site)')
    run('git pull origin master')
    restart()
    
def restart():
    run('$(root)$(site)/apache2/bin/restart')