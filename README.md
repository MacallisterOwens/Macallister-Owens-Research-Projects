# Research-Projects

## First Setup

Create your virtual env:
`python -m venv venv`

Enter the virtual env:
  * \*nix
`source venv/bin/activate`
  * Windows
`/venv/Scripts/activate`

If you are using git bash on windows it is `source venv/Scripts/activate`

Your terminal will look like `(venv) ~/PATH/TO/DIR`

Install django in the venv
`pip install django`

## Every other time

Enter your virtual env:
  * \*nix
`source venv/bin/activate`
  * Windows
`/venv/Scripts/activate`

#### Update the db by adding all migrations
`python manage.py migrate`

If you make any changes to the db models
`python manage.py makemigrations hmsSite`

To run the website
`python manage.py runserver`

To exit the venv
`deactivate`

Will launch it on [127.0.0.1:8000](http://127.0.0.1:8000/)

### Populate your database using fixtures
The fixtures are split into 3 different fixtures.
  * `admin_backup.json` contains all the data for users, schools, faculties, permissions, roles, and content types
  * `showcase_projects_backup.json` contains all the data for the nice looking showcase projects
  * `testing_projects_backup.json` contains all the data for the Lorem Ipsum projects made for testing

To create a fresh database first delete the `db.sqlite3` file from your local repo then run `python manage.py migrate`, then finally `python manage.py loaddata admin_backup.json {showcase_projects_backup.json | testing_projects_backup.json}` replacing `{showcase_projects.json | testing_projects_backup.json}` with whichever backup you wish.

Note: If you want to load in both project backups you can simply run `python manage.py loaddata admin_backup.json showcase_projects_backup.json testing_projects_backup.json`

### Using requirements.txt file to setup your VENV with the reuirements
`pip install -r requirements.txt`
this sets up your VENV with all the dependencies needed to run our project.
If anybody uses pip to install other packages then run:
`pip freeze > requirements.txt`
and push this file to the git repository, this will keep track of all packages as changed.

### Some git stuff

Install the repository onto your local drive
`git clone https://github.com/MacallisterOwens/Research-Projects-2.0.git`


Check the status, tells you what files have been changed etc.
`git status`

Add all your changes
`git add *`

Commit your changes
`git commit -m "MESSAGE"`

#### When you are finished with your feature in your branch

Checkout master and pull origin/master to ensure it is up to date
`git checkout master`
`git pull origin master`

Checkout the branch you did your work on
`git checkout BRANCH`

Merge master into your branch and resolve any conflicts
`git merge master`

Git push your branch onto the remote repository
`git push`

Create a pull request on GitHub for others to review

### How to run Celery periodic tasks on your local machine (Linux/Mac only)

  * Step 1:
  Install redis through the following commands:
  `sudo apt install redis-tools`
  `sudo apt install redis-server`
  * Step 2:
  Start the Redis server through `redis-server` and ensure it is running through `redis-ping` (You should get a `PONG` back)
  * Step 3:
  Ensure you run migrations so that the Celery db entries are created
  * Step 4:
  Run the following command **before** you start the Django server
  `celery -A app beat -l INFO --broker redis://localhost:6379/0 --scheduler django_celery_beat.schedulers:DatabaseScheduler`
  * Step 5:
  Run your Django server and Celery should be working in the background. If you don't want Celery to type out to your terminal remove the `-l INFO` from the previous command
 

### Accessing the website hosted on Azure

URL: https://researchprojectsdemo.azurewebsites.net/

User Logins: Removed for security reasons
  
