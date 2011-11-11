#!/bin/bash
set -e
cd /home/journal/webapps/journal/apps
source ../bin/activate
exec /home/journal/webapps/journal/apps/manage.py update_index
