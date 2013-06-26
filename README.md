SweetFeedback Server

Installation Steps:

1. MySQL, Python 2.7

Installing MySQL on Mac OS X
http://ihower.tw/rails3/advanced-installation.html

2. Required Python libraries:

Flask v0.9: web framework 
http://flask.pocoo.org/
pip install flask

Flask-SQLAlchemy v0.16:
pip install Flask-SQLAlchemy

Celery v3.0.19:
http://www.celeryproject.org/
pip install celery

MySQL-Python v1.2.4:
http://sourceforge.net/projects/mysql-python/
pip install MySQL-Python

GCM:
https://github.com/geeknam/python-gcm
pip install python-gcm

3. Database:
create a database SweetFeedback, then import the script 'sweetfeedback.sql'
It should create tables in your database.


4. Chagne config.py.dist to config.py and change user and password for database connection.


5. Execute app.py to start up the server.
python app.py

