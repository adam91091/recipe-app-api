#!/bin/sh

# force failing script if any commands would fail in this script
set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

# run uwsgi service - port 9000 is used by proxy to connect app server
# workers numbers should be related to cpu capabilities
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi