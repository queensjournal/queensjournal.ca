#!/bin/bash

# Gunicorn start script
set -e
LOGFILE=/home/journal/logs/journal-gunicorn.log
NUM_WORKERS=3
# user/group to run as
USER=journal
source /home/journal/journal/bin/activate
exec /home/journal/journal/bin/gunicorn_django -w $NUM_WORKERS \
    --user=$USER --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE
