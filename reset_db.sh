#!/bin/sh

DBNAME=od
DBUSER=od

sudo su postgres -c "dropdb $DBNAME"
sudo su postgres -c "createdb -O $DBUSER $DBNAME"
python manage.py syncdb --noinput
python manage.py migrate
