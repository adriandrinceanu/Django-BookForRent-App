#!/bin/bash
export DJANGO_SETTINGS_MODULE=BookForRent.settings

python manage.py makemigrations 
python manage.py migrate 
python manage.py createsuperuser --no-input
python manage.py collectstatic --no-input
# python manage.py loaddata db.json
# python manage.py runserver 0.0.0.0:8000

gunicorn --config gunicorn-cfg.py BookForRent.wsgi -b 0.0.0.0:8000