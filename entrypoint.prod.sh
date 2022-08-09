#!/bin/sh

echo "initializing EIEI ...................."
# python manage.py flush --no-input
python manage.py collectstatic
python manage.py migrate

exec "$@"
