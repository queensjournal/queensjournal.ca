#!/bin/bash

# link nginx
sudo ln -s journal-nginx.conf /etc/nginx/conf.d/

# link gunicorn
sudo ln -s journal-gunicorn.conf /etc/supervisor/conf.d/

sudo ln -s journal-memcached.conf /etc/supervisor/conf.d/