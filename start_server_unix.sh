#!/bin/bash
echo 'Starting Server'
source venv-unix/bin/activate && python manage.py migrate && python manage.py loaddata admin_backup.json showcase_projects_backup.json && python manage.py runserver
