#!/bin/bash

# Gunicorn start script
set -e
LOGFILE=/home/journal/logs/journal-guinicorn.log
NUM_WORKERS=3
# user/group to run as
USER=journal
cd /home/journal/webapps/journal/apps
source ~/webapps/journal/bin/activate
exec /home/journal/webapps/journal/bin/gunicorn_django -w $NUM_WORKERS \
    --user=$USER --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE
