@echo OFF
echo.
echo.
echo Starting server
REM this enters vm, loads data, starts server
call venv\Scripts\activate && python manage.py migrate && python manage.py loaddata admin_backup.json showcase_projects_backup.json && python manage.py runserver
