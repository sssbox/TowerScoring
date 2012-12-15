This project uses several sound effects from freesound.org, some of which have been modified by Sam Solomon. For a list, please see media/sfx/README

## Install git

`sudo apt-get install git-core`

## Set up github on your work computer 

* [http://help.github.com/linux-set-up-git/](http://help.github.com/linux-set-up-git/)
https://github.com/sssbox/TowerScoring/edit/master/README.md#

## Get the repo

```bash
git clone git@github.com:sssbox/TowerScoring.git
mv TowerScoring scoring
cd scoring
```

## Install some system requirements

sudo apt-get install -y mysql-server
sudo apt-get install -y python-pip
sudo apt-get install -y python-mysqldb
sudo apt-get install -y python-profiler
sudo apt-get install -y libtidy-dev
sudo apt-get install -y libmysqlclient-dev

## install virtualenv(wrapper) and then create a virtualenv for scoring

```bash
sudo pip install virtualenv
sudo pip install virtualenvwrapper

mkvirtualenv scoring --no-site-packages
deactivate
workon scoring
```
The last two lines aren't necessary, but are for informational purposes (Every time you run `runserver` or `syncdb` or `migrate` you will need to `workon scoring` to activate the virtualenv.


```bash
pip install -r requirements.txt

touch local_settings.py
```

### In mysql:

```mysql
create database scoring;
CREATE USER 'scoring'@'localhost' IDENTIFIED BY '304c78aeeedec74b14d42a2324448f39';
GRANT ALL PRIVILEGES ON scoring.* TO 'scoring'@'localhost';
```

```bash
python manage.py syncdb #Create superuser when prompted
python manage.py migrate
```

~~~ Optionally you may add things to local_settings.py file to override settings locally--this does not get tracked so they will only effect your install.

```bash
python manage.py runserver_plus <your ip>:8000
```

Getting some stuff to work:
log into http://<your ip>:8000/admin/
Open in a new tab http://<your ip>:8000/ you should see the scorekeeper display (the migrations add the first user that exists in the database (the superuser you created with syncdb) to the scorekeeper group which makes the awesome scorekeeper display the screen you see at the homepage)

click 'Users'

Add user "sk1" (with a short password) click "Save and continue editing"
Make that user "Staff status" and add them to the "Scorers" group then click "save"
* If you want you can repeat three more times for extra scorers


Add user "timer" (with a good password) click "Save and continue editing"
Make user "Staff status" AND add them to the group "Displays" before saving

Back at the scorekeeper homepage, refresh to get all your new scorers in the "Scorer" drop down menus, assign your scorers to the different goals.


Open a different browser (Firefox vs Chrome (incognito doesn't work with django's dev server for some reason)) and go to http://<your ip>:8000/
Log in as 'timer'

Use your phone on your wifi to go to http://<your ip>:8000/ and log in as a scorer.

From the original superuser account on the scorekeeper display start a match and play with other stuff like that.

# Notes

For the actual (non-dev) install you will probably need to set this up with apache and you will definitely also need to install Celery to handle sound/lighting
