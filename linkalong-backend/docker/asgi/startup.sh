#!/usr/bin/env bash

set -e

python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput

daphne -b 0.0.0.0 -p 8000 linkalong.asgi:application
