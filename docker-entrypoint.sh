#!/bin/bash
# /data/backend/mmtxt/bin/python /data/backend/backend/manage.py makemigrations usermanagement
# /data/backend/mmtxt/bin/python /data/backend/backend/manage.py makemigrations organization
# /data/backend/mmtxt/bin/python /data/backend/backend/manage.py makemigrations project
# /data/backend/mmtxt/bin/python /data/backend/backend/manage.py makemigrations operations
/data/backend/mmtxt/bin/python /data/backend/backend/manage.py migrate usermanagement
/data/backend/mmtxt/bin/python /data/backend/backend/manage.py migrate organization
/data/backend/mmtxt/bin/python /data/backend/backend/manage.py migrate project
# /data/backend/mmtxt/bin/python /data/backend/backend/manage.py migrate operations
chmod 777 -R /data/backend/backend
mkdir -p /data/backend/media_files
chmod 777 /data/backend/media_files
mkdir -p /data/backend/backend/logs
service supervisor start
apache2ctl -D FOREGROUND
