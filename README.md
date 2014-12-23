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

    [trusted]
    users = root

* Installing the PostgreSQL module failed pointing to absence of pg_config, and installing libpq-dev corrected this.

* Compiling the MySQL module failed and referred to a missing Python.h.  Installing libpython2.7-dev fixed this.

To update database tables:
    
    # Locally
    python manage.py schemamigration users --initial
    python manage.py schemamigration users --auto
    python manage.py schemamigration users --help

    # On Heroku - Production/Staging
    heroku run python manage.py migrate userorganization --app mycleancity-staging

To dump fixtures

    python manage.py dumpdata --indent 2 cleanteams.cleanteamlevel cleanteams.cleanteamleveltask challenges.challengetype challenges.cleangrid challenges.challengequestiontype challenges.answertype challenges.challengequestion challenges.questionanswer notifications.notification > fixtures/initial_data.json

To load fixtures

    python manage.py loaddata fixtures/initial_data.json

To run the django development server, you will first need to setup the database:

    python manage.py syncdb

This loads default data into the database as defined by fixtures within
the `users` app.

If running locally, open settings.py and comment out:

    DATABASES['default'] = dj_database_url.config()

Also, change:

    DEBUG = False to DEBUG = True
    
Uncomment the following line 
 
    AWS_BUCKET = 'mycleancitystaging'

* _[Zeeshan Syed](https://bitbucket.org/syedzee) knows a more efficient way of doing this, but he didn't have time._

At this point you are ready to run the development server:

    python manage.py runserver 0.0.0.0:10000

Above, the `--noreload` argument is optional, and prevents django from reloading
every time you make a code change. Now the development web server should be
running. Try it by connecting via a web browser:

    http://localhost:10000

* _Running *manage.py syncdb* produces an error,_
~~~~
(venv)ilgiz@ei:~/work/my-clean-city$ python manage.py syncdb
Syncing...
Creating tables ...
Creating table auth_permission
Creating table auth_group_permissions
Creating table auth_group
Creating table auth_user_groups
Creating table auth_user_user_permissions
Creating table auth_user
Creating table django_content_type
Creating table django_session
Creating table django_admin_log
Creating table south_migrationhistory

You just installed Django's auth system, which means you don't have any superusers defined.
Would you like to create one now? (yes/no): yes
Username (leave blank to use 'ilgiz'):
Email address: ilatypov@yahoo.ca
Password:
Password (again):
DatabaseError: (1146, "Table 'mycleancity.userprofile_userprofile' doesn't exist")
~~~~
** Following a Stack Overflow answer to [Can't Create Super User Django](http://stackoverflow.com/questions/14059573/cant-create-super-user-django), the syncdb proceeds but migrate fails in altering a table `challenges_challenge`,
~~~~
(venv)ilgiz@ei:~/worktmp/my-clean-city$ sudo mysqladmin drop mycleancity
Dropping the database is potentially a very bad thing to do.
Any data stored in the database will be destroyed.

Do you really want to drop the 'mycleancity' database [y/N] y
Database "mycleancity" dropped
(venv)ilgiz@ei:~/worktmp/my-clean-city$ sudo mysqladmin create mycleancity
(venv)ilgiz@ei:~/worktmp/my-clean-city$ python manage.py syncdb --noinput
Syncing...
Creating tables ...
Creating table auth_permission
Creating table auth_group_permissions
Creating table auth_group
Creating table auth_user_groups
Creating table auth_user_user_permissions
Creating table auth_user
Creating table django_content_type
Creating table django_session
Creating table django_admin_log
Creating table south_migrationhistory
Installing custom SQL ...
Installing indexes ...
Installed 0 object(s) from 0 fixture(s)

Synced:
 > django.contrib.auth
 > django.contrib.contenttypes
 > django.contrib.sessions
 > django.contrib.messages
 > django.contrib.staticfiles
 > django.contrib.admin
 > django.contrib.admindocs
 > django_mobile
 > django_wysiwyg
 > captcha
 > south
 > storages

Not synced (use migrations):
 - django_extensions
 - cleancreds
 - cleanteams
 - challenges
 - notifications
 - users
 - userorganization
 - userprofile
(use ./manage.py migrate to migrate these)
(venv)ilgiz@ei:~/worktmp/my-clean-city$ python manage.py migrate
Running migrations for django_extensions:
 - Migrating forwards to 0001_empty.
 > django_extensions:0001_empty
 - Loading initial data for django_extensions.
Installed 0 object(s) from 0 fixture(s)
Running migrations for cleancreds:
 - Migrating forwards to 0001_initial.
 > cleancreds:0001_initial
 - Loading initial data for cleancreds.
Installed 0 object(s) from 0 fixture(s)
Running migrations for cleanteams:
 - Migrating forwards to 0040_auto__add_field_cleanteam_contact_user__add_field_cleanteam_contact_ph.
 > cleanteams:0001_initial
 > cleanteams:0002_auto__add_cleanteammember
 > cleanteams:0003_auto__del_cleanteammember
 > cleanteams:0004_auto__add_cleanteammember
 > cleanteams:0005_auto__chg_field_cleanteammember_status
 > cleanteams:0006_auto__del_cleanteammember
 > cleanteams:0007_auto__add_cleanteammember
 > cleanteams:0008_auto__add_field_cleanteam_about
 > cleanteams:0009_auto__add_field_cleanteammember_role
 > cleanteams:0010_auto__add_field_cleanteam_twitter
 > cleanteams:0011_auto__add_field_cleanteam_region__add_field_cleanteam_team_type__add_f
 > cleanteams:0012_auto__chg_field_cleanteam_region
 > cleanteams:0013_auto__chg_field_cleanteam_region
 > cleanteams:0014_auto__del_field_cleanteam_region
 > cleanteams:0015_auto__del_field_cleanteam_team_type
 > cleanteams:0016_auto__del_field_cleanteam_group
 > cleanteams:0017_auto__add_field_cleanteam_region__add_field_cleanteam_team_type__add_f
 > cleanteams:0018_auto__add_cleanteampost
 > cleanteams:0019_auto__add_cleanchampion
 > cleanteams:0020_auto__add_cleanteaminvite
 > cleanteams:0021_auto__add_field_cleanteaminvite_email
 > cleanteams:0022_auto__add_field_cleanteaminvite_token
 > cleanteams:0023_auto__chg_field_cleanteaminvite_token
 > cleanteams:0024_auto__add_cleanteamlevelprogress__add_cleanteamlevel__add_cleanteamlev
 > cleanteams:0025_auto__add_field_cleanteam_level
 > cleanteams:0026_auto__del_field_cleanteamlevel_level__add_field_cleanteamlevel_name
 > cleanteams:0027_auto__add_field_cleanteamlevel_next_level
 > cleanteams:0028_auto__chg_field_cleanteam_level
 > cleanteams:0029_auto__del_field_cleanteam_level
 > cleanteams:0030_auto__add_field_cleanteam_level
 > cleanteams:0031_auto__add_field_cleanteamleveltask_name
 > cleanteams:0032_auto__add_unique_cleanteamleveltask_name
 > cleanteams:0033_auto__add_field_cleanteamlevel_tree_level
 > cleanteams:0034_auto__add_field_cleanteamleveltask_link
 > cleanteams:0035_auto__add_leaderreferral
 > cleanteams:0036_auto__add_field_leaderreferral_timestamp__add_field_leaderreferral_cle
 > cleanteams:0037_auto__add_field_cleanteamlevelprogress_approval_requested__add_field_c
 > cleanteams:0038_auto__add_cleanteampresentation
 > cleanteams:0039_auto__add_field_cleanteam_admin
 > cleanteams:0040_auto__add_field_cleanteam_contact_user__add_field_cleanteam_contact_ph
 - Loading initial data for cleanteams.
Installed 0 object(s) from 0 fixture(s)
Running migrations for challenges:
 - Migrating forwards to 0064_auto__chg_field_cleanteamchallenge_total_hours__chg_field_cleanteamcha.
 > challenges:0001_initial
 > challenges:0002_auto__chg_field_userchallenge_timestamp__del_field_challenge_datetime_
/mnt/wd-mypassportultra/work/my-clean-city/venv/local/lib/python2.7/site-packages/django/db/models/fields/__init__.py:827: RuntimeWarning: DateTimeField received a naive datetime (2013-09-22 00:00:00) while time zone support is active.
  RuntimeWarning)

 > challenges:0003_auto__chg_field_challenge_event_datetime
 > challenges:0004_auto__del_field_challenge_event_datetime__add_field_challenge_event_da
 > challenges:0005_auto__chg_field_challenge_event_time__chg_field_challenge_user__del_un
FATAL ERROR - The following SQL query failed: ALTER TABLE `challenges_challenge` MODIFY `event_time` time NULL;;
The error was: (1025, "Error on rename of './mycleancity/#sql-75d_4d' to './mycleancity/challenges_challenge' (errno: 150)")
 ! Error found during real run of migration! Aborting.

 ! Since you have a database that does not support running
 ! schema-altering statements in transactions, we have had
 ! to leave it in an interim state between migrations.

! You *might* be able to recover with:   - no dry run output for alter_column() due to dynamic DDL, sorry
   - no dry run output for alter_column() due to dynamic DDL, sorry
   = ALTER TABLE `challenges_challenge` ADD CONSTRAINT `challenges_challenge_user_id_1e3f3129_uniq` UNIQUE (`user_id`) []
   - no dry run output for alter_column() due to dynamic DDL, sorry

 ! The South developers regret this has happened, and would
 ! like to gently persuade you to consider a slightly
 ! easier-to-deal-with DBMS (one that supports DDL transactions)
 ! NOTE: The error which caused the migration to fail is further up.
Error in migration: challenges:0005_auto__chg_field_challenge_event_time__chg_field_challenge_user__del_un
DatabaseError: (1025, "Error on rename of './mycleancity/#sql-75d_4d' to './mycleancity/challenges_challenge' (errno: 150)")
(venv)ilgiz@ei:~/worktmp/my-clean-city$ mysql -Dmycleancity -e "show tables"
+-----------------------------------+
| Tables_in_mycleancity             |
+-----------------------------------+
| auth_group                        |
| auth_group_permissions            |
| auth_permission                   |
| auth_user                         |
| auth_user_groups                  |
| auth_user_user_permissions        |
| challenges_userchallenge          |
| cleancreds_cleancredsachievements |
| cleancreds_cleancredsmilestones   |
| cleanteams_cleanchampion          |
| cleanteams_cleanteam              |
| cleanteams_cleanteaminvite        |
| cleanteams_cleanteamlevel         |
| cleanteams_cleanteamlevelprogress |
| cleanteams_cleanteamleveltask     |
| cleanteams_cleanteammember        |
| cleanteams_cleanteampost          |
| cleanteams_cleanteampresentation  |
| cleanteams_leaderreferral         |
| django_admin_log                  |
| django_content_type               |
| django_session                    |
| south_migrationhistory            |
+-----------------------------------+
(venv)ilgiz@ei:~/worktmp/my-clean-city$ mysql -Dmycleancity -e 'ALTER TABLE `challenges_challenge` MODIFY `event_time` time NULL'
ERROR 1146 (42S02) at line 1: Table 'mycleancity.challenges_challenge' doesn't exist
~~~~
