This project uses several sound effects from freesound.org, some of which have been modified by Sam Solomon. For a list, please see media/sfx/README

## Install git

`sudo apt-get install git-core`

## Set up github on your work computer 

* [http://help.github.com/linux-set-up-git/](http://help.github.com/linux-set-up-git/)

## Get the repo

```bash
git clone git@github.com:sssbox/TowerScoring.git
mv TowerScoring scoring
cd scoring
```

## Install some system requirements

```bash
sudo apt-get install -y mysql-server
sudo apt-get install -y python-pip
sudo apt-get install -y python-mysqldb
sudo apt-get install -y python-profiler
sudo apt-get install -y libtidy-dev
sudo apt-get install -y libmysqlclient-dev
```

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

touch scoring/local_settings.py
```

### In mysql:

```mysql
create database scoring;
CREATE USER 'scoring'@'localhost' IDENTIFIED BY '304c78aeeedec74b14d42a2324448f39';
GRANT ALL PRIVILEGES ON scoring.* TO 'scoring'@'localhost';
```

### Back from the standard bash prompt (with the 'scoring' virtualenv enabled (`workon scoring`)

```bash
python manage.py syncdb #Create superuser when prompted
python manage.py migrate
```

## Collecting static files

Before trying the server and wWenever you add/modify static media in scoring/match/static or scoring/*/static you need to run:

```bash
python manage.py collectstatic
```

~~~ Optionally you may add things to scoring/local_settings.py file to override settings locally--this does not get tracked so they will only effect your install.

## Start the server

* Using 0.0.0.0 as the ip to bind to means it will be listening on all interfaces so you can use [http://127.0.0.1:8000](http://127.0.0.1:8000) or [http://localhost:8000](http://localhost:8000) from your local machine or `http://<your_ip>:8000` from your machine or any other computer on your network (also useful for testing as even without going to incognito you can have 3 different sessions, one each for those 3 urls (and 6 if you use incognito, 12 if you use incognito on both Chrome and Chromium, and 18 if you also use firefox (though do they still do that thing where you can't browse "in private" and not in private in parallel?).

```bash
python manage.py runserver 0.0.0.0:8000
```

## Getting some stuff to work:

log into `http://localhost:8000/admin/`

Open in a new tab `http://localhost:8000/` you should see the scorekeeper display (the migrations add the first user that exists in the database (the superuser you created with syncdb) to the scorekeeper group which makes the awesome scorekeeper display the screen you see at the homepage)

Back in the admin:

Change all timer/display passwords (normally you can change them by clicking the following link, saving and then changing the 2 to 3-6 for the scorer users.)
* [http://localhost:8000/admin/auth/user/2/password/](http://localhost:8000/admin/auth/user/2/password/)

Back at the scorekeeper homepage, assing the scorers with the "Scorer" drop down menus.


Open a different browser and go to http://localhost:8000/

Log in as 'timer'

Use your phone on your wifi to go to `http://<your ip>:8000/` and log in as a scorer_1 (or _2, _3, or _4).

From the original superuser account on the scorekeeper display start a match and play with other stuff like that.

# Notes

For the actual (non-dev) install you will probably need to set this up with apache and you will definitely also need to install Celery to handle sound/lighting

See [docs/production_setup.md](docs/production_setup.md) for details.
