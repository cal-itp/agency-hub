#!/bin/bash -e

if [ -n "${DJANGO_MIGRATE_ON_STARTUP}" ]; then
    python manage.py migrate
fi

exec python manage.py runserver "0.0.0.0:${PORT:-8000}"
