##SweetFeedback Server

###Installation Steps:

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

###Server API documentation(How to use)###

####http://209.129.244.24:1234/bluetooth_around####

Method: GET

Parameters:
	
	bluetooth_id: 
		the bluetooth mac address discovered.
	device_name: 
		the bluetooth device name.
	device_id: 
		the device_id that capable of bluetooth discovering.
Return: The json of inserted data in device_around table.

ex. 
 
	
####To get candies, we have three steps.

1. We need to start client application on client computer and know the device_id of the gumball machine. 
2. Once your application is about to distribute feedback, use insert_feedback/ to insert the feedback. 
3. You get candies from the machine with device_id you provided in step1.

####http://209.129.244.24:1234/insert_feedback
This api will insert a feedback into repository in our database.
 
Method: GET

Parameters:

	device_id: 
		the device id of your gumball machine.
	application_id: 
		the application id of your application.
	user_id(optional): 
		your user_id.
	feedback_type: 
		type of feedback(positive/negative).
	feedback_description: 
		the description of feedback.
####http://209.129.244.24:1234/get_feedback 
This api is for gumball machine to call. 
####http://209.129.244.24:1234/update_feedback
####http