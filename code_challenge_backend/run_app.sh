#!/bin/sh
while ! nc -w 1 -z db 5432; do
    echo "Wating for postgres"
    sleep 11
done;

python manage.py migrate

while :; do 
    python manage.py runserver 0.0.0.0:8000
    sleep 1
done
