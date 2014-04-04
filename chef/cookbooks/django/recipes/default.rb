::Chef::Recipe.send(:include, Opscode::OpenSSL::Password)

users = data_bag("users")

# create deploy group
group "deploy" do
  gid 123
end

users.each do |user|
  u = data_bag_item('users', user)

  log "creating user #{u['id']}"
  user u['id'] do
    username u['id']
    shell u[:shell] || "/bin/bash"
    home "/home/#{u['id']}"
    group "deploy"
  end

  directory "/home/#{u['id']}" do
    owner u['id']
    group "deploy"
    mode 0700
  end

  directory "/home/#{u['id']}/.ssh" do
    owner u['id']
    group "deploy"
    mode 0700
  end

  u['ssh_keys'].each do |key|
    execute "authorized keys" do
      command "echo #{key} >> /home/#{u['id']}/.ssh/authorized_keys"
    end
  end
end

user 'www-data' do
  group "deploy"
end

# setup app directory
app_path = File.expand_path("/opt/journal")
repo_path = File.expand_path("/opt/journal.git")

directory app_path do
  owner "www-data"
  group "deploy"
  mode 0770
end

directory repo_path do
  owner "www-data"
  group "deploy"
  mode 0770
end

execute "setup git repo" do
  cwd repo_path
  command "git init --bare --shared"
end

template "#{repo_path}/config" do
  source "git-config.erb"
  group "deploy"
end

template "#{repo_path}/hooks/post-receive" do
  source "post-receive.erb"
  mode 01755
  variables({
    :app_path => app_path,
    :manage_py => File.join(app_path, 'manage.py')
  })
end

#[repo_path, app_path].each do |path|
  #execute "group permissions" do
    #cwd "#{path}"
    #command "chgrp -R deploy ."
  #end

  #execute "repo permissions" do
    #cwd "#{path}"
    #command "chown -R deploy ."
  #end
#end

include_recipe "postgresql::server"
include_recipe "postgresql::server_dev"

node.set_unless[:postgres][:password] = secure_password

pg_user "journal" do
  privileges superuser: false, createdb: false, login: true
  password node[:postgres][:password]
end

pg_database "journal" do
  owner "journal"
end

include_recipe "python"

ve = python_virtualenv "journal" do
  path "/opt/journal/venv"
  owner "www-data"
  group "deploy"
  action :create
end

# PIL dependencies
package "libjpeg8"
package "libjpeg-dev"
package "libfreetype6"
package "libfreetype6-dev"
package "zlib1g-dev"

# xapian dependencies
package 'libxapian22'
package 'libxapian-dev'
package 'python-xapian'

# ve.path
link "#{ve.path}/lib/python2.7/site-packages/xapian" do
  to "/usr/lib/python2.7/dist-packages/xapian" 
end

directory "#{app_path}/xapian" do
  owner "www-data"
  group "deploy"
  mode 0775
end

node.set_unless[:django][:secret_key] = secure_password(50)

directory "#{app_path}/journal" do
  owner "www-data"
  group "deploy"
  mode 0775
end

execute "app permissions" do
  cwd "#{app_path}"
  command "chmod -R 0770 ."
end

# settings_local
template "#{app_path}/journal/settings_local.py" do
  source "settings_local.erb"
  owner "www-data"
  group "deploy"
  variables({
    :app_path => app_path,
    :db => 'journal',
    :db_user => 'journal',
    :db_pass => node[:postgres][:password],
    :secret_key => node[:django][:secret_key],
  })
  notifies :restart, "runit_service[django]"
end

runit_service "django" do
  options({
    :user => 'www-data',
    :gunicorn_path => File.join(ve.path, 'bin/gunicorn'),
    :app_path => app_path,
    :app => 'journal'
  })
end

template "/etc/nginx/sites-available/journal" do
  source "nginx-journal.erb"
  owner "www-data"
  variables({
    :app_path => app_path,
  })
  notifies :reload, "service[nginx]", :delayed
end

link "/etc/nginx/sites-enabled/journal" do
  to "/etc/nginx/sites-available/journal"
end

%w[ /served /served/static /served/media ].each do |path|
  directory "#{app_path}#{path}" do
    owner "www-data"
    group "deploy"
    mode 0770
  end
end

include_recipe "apt"

apt_repository 'node-js' do
  uri 'http://ppa.launchpad.net/chris-lea/node.js/ubuntu'
  distribution 'precise'
  components ['main']
  notifies :install, 'package[nodejs]', :immediately
end

package 'nodejs'
