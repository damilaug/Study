#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate


# set -o errexit
# pip install -r requirements.txt 
# python manage.py collectstatic --no-input
# python manage.py migrate