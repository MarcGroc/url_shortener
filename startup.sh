#!/usr/bin/env bash
echo  "Running a startup script..."
set -e

python  manage.py check_db
python manage.py check_or_create_user
python  manage.py migrate
python  manage.py makemigrations

echo  "Startup complete."