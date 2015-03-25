# My Effect

The aim is to have django models for all key data to power all website operations

## Requirements

A basic understanding of the following is required:

    pip
    python
    mysql
    south
    django
    git
    git-flow
    heroku

## Repository

To clone from bitbucket.org, make sure you have access to the project and type:

    git clone git@bitbucket.org:hakstudio/my-clean-city.git

To pull from bitbucket.org, make sure you have access to the project and type:

    git pull origin master
    git pull origin develop

Setup git flow by typing:

    git flow init

Follow the instructions, and leave all of the branch names as their default (ie. master, develop, release, etc.)
Version tagging prefix is v-

## Hosting

Hosting of the application is done on Heroku. Kelly's host would have required
too much setup.

    The Heroku apps are as follows:
    
    mycleancity-staging - Staging (Test)
    mycleancity - Production (Live)

    Be sure to add these remotes to your git repo project

To push to Staging, type:
    
    git push staging develop:master # If you wanted to push the develop branch

or
    
    git push staging master # If you wanted to push the master branch

To push to Production, type:
    
    git push heroku master

Both apps should be transferred in Heroku to the developers Heroku account.

## Getting Started

To get started, clone the git repo to your local workstation.

Included in this config file is the database information. You may need to
install MySQL at this point, and create a new database.

Next, create a local version of python.

    virtualenv -p python2.7 venv

Put the local version of Python in your path.
(You will have to do this every time you use the project.)

    source venv/bin/activate

To stop using the local version of python:

    deactivate

To install Django Heroku-Toolbelt:
	
	pip install django-toolbelt

To install all python requirements:
    
    pip install --requirement requirements.txt

* Python-MySQL 1.2.4 failed to install on Debian sid due to an error, "maximum recursion depth exceeded". Using Python-MySQL 1.2.5 appears to work.  At some point, installation will require mysql_config from libmysqlclient-dev.

* The mysql connector refused to download an untrusted package, and ignoring this concern by prefixing the name of the package with "--allow-external" in requirements.txt worked this around.

* The hg command from the Debian mercurial package failed to showconfig paths.default stored in venv/src/pil/.hg/hgrc.  Creating a ~/.hgrc with a trust to root helps,
~~~~
[trusted]
users = root
~~~~
* Installing the PostgreSQL module failed pointing to absence of pg_config, and installing libpq-dev corrected this.

* Compiling the MySQL module failed and referred to a missing Python.h.  Installing libpython2.7-dev fixed this.

* Running "manage.py createsuperuser" showed an error about a missing JPEG handler.  Installing respective libraries, re-installing the Python pillow module fixed that,
~~~~
sudo apt-get install libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev
pip uninstall pillow
pip install -r requirements.txt
~~~~

If running manage.py locally, you'll need to specify which settings file to use.  You can create your own, or use someone elses.  

In our project each stage (production and staging) and each person will have their own settings.py file.  This is necessary as the project scales, and it will prevent us from pushing incorrect configuration values and breaking our production stage (since each of us will have a different db password, differnt setup etc.)  It also prevents from breaking each others local configuration. Production and staging are also different, so they need separate settings files.  It also prevents us from corrupting production data easily, if we accidentally talked to the wrong S3 bucket, since these need to be specified differently in production/staging settings.

As a result you'll need to indicate which settings.py file to use.

This is documented here:

https://docs.djangoproject.com/en/1.7/topics/settings/

For those of us on linux, you can just push an export in your .bashrc:

export DJANGO\_SETTINGS\_MODULE=mycleancity.<yourname>\_settings

Otherwise, you can just use --setings-file=... when you run command line statements.


* Creating a database failed to alter a time field.  Fix:
* * Update Django to the latest release 1.7.1.
* * Remove "south" from requirements.txt and from settings.py.
* * Remove `*/migrations/*.py*` except `*/migrations/__init__.py`.
* * Run "python manage.py makemigrations", "python manage.py migrate".

* Creating the database failed in serializing a timezone field.  Updating django-timezone-field to a newer version resolved this.


To update database tables:

~~~~    
# Locally
python manage.py schemamigration users --initial
python manage.py schemamigration users --auto
python manage.py schemamigration users --help

# On Heroku - Production/Staging
heroku run python manage.py migrate userorganization --app mycleancity-staging
~~~~

To dump fixtures
~~~~
python manage.py dumpdata --indent 2 cleanteams.cleanteamlevel cleanteams.cleanteamleveltask challenges.challengetype challenges.cleangrid challenges.challengequestiontype challenges.answertype challenges.challengequestion challenges.questionanswer notifications.notification > fixtures/initial_data.json
~~~~

To load fixtures
~~~~
python manage.py loaddata fixtures/initial_data.json
~~~~

To run the django development server, you will first need to setup the database:
~~~~
python manage.py syncdb
~~~~

This loads default data into the database as defined by fixtures within
the `users` app.



At this point you are ready to run the development server:
~~~~
python manage.py runserver 0.0.0.0:10000
~~~~
Above, the `--noreload` argument is optional, and prevents django from reloading every time you make a code change. Now the development web server should be running. Try it by connecting via a web browser:
~~~~
http://localhost:10000
~~~~
* The error about a missing Python module in an import statement may result from forgetting to source venv/bin/activate.

To delete your entire local database and start over:

#  This files will show you how to re-create your database from scratch and re-run all migrations.
#  This is also useful when setting up the database the first time


--  Will delete all user data!!! Do not run this on production or staging!
#  Log into mysql first
drop database mycleancity;  #  Don't need to do this if you're setting up for first time
create database mycleancity;

#  On command line
#  This will create some basic stuff like the south migration table and some other tables
python manage.py syncdb
#  Apply all migrations that come with the project
python manage.py migrate --all
#  Populate database with basic information like team levels etc.
python manage.py loaddata fixtures/initial_data.json
