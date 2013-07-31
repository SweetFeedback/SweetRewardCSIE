from flask import Flask, Blueprint, render_template, request, jsonify, json
from celery import Celery 
from tasks import add

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from sqlalchemy.sql import func
from model import *
import config
from members import *
from datetime import datetime, timedelta
import time
import pytz
import json 
import urllib2
from random import choice

#blueprint
api = Blueprint('api', __name__)
@api.route("/sensor_log_index/<device_id>")
def get_sensor_log(device_id):
	sensor_log_index = db.session.query(GumballSensorIndex).filter_by(device_id=device_id).first()
	if sensor_log_index is None: 
		return jsonify(nodata="no this data")
	else:
		return jsonify(data=sensor_log_index.serialize)

@api.route("/sensor_log_index")
def get_all_sensor_log():
	# last seen data 
	sensor_log_indexs = db.session.query(GumballSensorIndex).all()
	return jsonify(data=[i.serialize for i in sensor_log_indexs])
@api.route("/sensor_log_index/online")
def get_online_sensor_log():
	online_devices = DeviceOnline.query.all()
	device_numbers = []
	sensor_log_index = [] 
	for online_device in online_devices: 
		d_id = int(online_device.device_id)
		device_numbers.append(d_id)
	sensor_log_indexs = db.session.query(GumballSensorIndex).all()
	for log in sensor_log_indexs: 
		if log.device_id in device_numbers:
			sensor_log_index.append(log)
	return jsonify(data=[i.serialize for i in sensor_log_index])

@api.route("/sensor_log/insert", methods=['GET'])
def sensor_insert():
	light_sensor = request.args.get("light_level", -1)
	sound_sensor = request.args.get("sound_level", -1)
	temp_sensor = request.args.get("temperature", -1)
	device_id = request.args.get("device_id", -1)
	
	if device_id != -1:
		device_login_or_update(device_id, request.remote_addr)
	else: 
		return jsonify(error="it's needed to provide device id.")
	if light_sensor != -1 and sound_sensor != -1 and temp_sensor != -1:
		sensor_log = GumballSensor(device_id, light_sensor, temp_sensor, sound_sensor)
		db.session.add(sensor_log)
		db.session.commit()
		indexs = db.session.query(GumballSensorIndex).filter_by(device_id=device_id).first()
		print indexs
		if indexs is None:
			sensor_log_index = GumballSensorIndex(sensor_log.log_id, sensor_log.device_id, sensor_log.light, sensor_log.temperature, sensor_log.sound)
			db.session.add(sensor_log_index)
			db.session.commit()
		else:
			indexs.log_id = sensor_log.log_id
			indexs.device_id = sensor_log.device_id
			indexs.sound = sensor_log.sound
			indexs.temperature = sensor_log.temperature
			indexs.light = sensor_log.light
			indexs.time = sensor_log.time
			db.session.commit()
	else:
		return jsonify(error="data not completed.")
	return jsonify(data=[sensor_log.serialize], index=[indexs.serialize])

@api.route("/check")
def check():
	deleted = check_online_device()
	return jsonify(deleted=[i.serialize for i in deleted])

def device_login_or_update(device_id, address):
	check_online_device()
	device_status = db.session.query(DeviceOnline).filter_by(device_id=device_id).first()

	if device_status is not None:
		print device_status.serialize
		device_status.time = datetime.now()
		db.session.commit()
	else:
		timestamp = datetime.now()
		device_status = DeviceOnline(device_id, timestamp, address)
		db.session.add(device_status)
		db.session.commit()
	return device_status
def check_online_device():
	devices = DeviceOnline.query.all()
	now = datetime.now()
	device_delete = []
	for device in devices: 
		diff =  (now - device.time).seconds / 60
		if diff > 1: ## 10 mins 
			db.session.delete(device)
			db.session.commit()
			device_delete.append(device)
	return device_delete	
@api.route("/online_device")
def get_online_device():
	devices = DeviceOnline.query.all()
	return jsonify(device=[i.serialize for i in devices])

def get_device_id_from_ip(address):
	device_id = -1
	device_status = db.session.query(DeviceOnline).filter_by(ipaddress=address).first()
	if device_status is not None: 
		device_id = device_status.device_id
	return device_id

# going to insert window_log data 
@api.route("/window_log/insert", methods=['GET', 'POST'])
def insert_window_log():
	location_id = request.args.get("location_id", -1)
	window_id = request.args.get("window_id", -1)
	state = request.args.get("state", -1)
	device_id = request.args.get("device_id", -1)
	if device_id != -1:
		device_login_or_update(device_id, request.remote_addr)

	window_log = Window(location_id, window_id, state)
	db.session.add(window_log)
	db.session.commit()

	# insert to window index table 	
	indexs = db.session.query(WindowIndex).filter_by(window_id=window_id).first()
	print indexs
	if indexs is None:
		window_index = WindowIndex(window_log.log_id, window_log.location_id, window_log.window_id, window_log.state, window_log.timestamp)
		db.session.add(window_index)
		db.session.commit()
	else:
		indexs.log_id = window_log.log_id
		indexs.location_id = window_log.location_id
		indexs.window_id = window_log.window_id
		indexs.state = window_log.state
		indexs.timestamp = window_log.timestamp
		db.session.commit()
		#print "update records"
	
	#print location_id, window_id, state
	return jsonify(data=[window_log.serialize])

@api.route("/window_log/<window_id>")
def get_all_extended_window_data(window_id):
	window_log = Window.query.filter(Window.window_id == window_id).order_by(desc(Window.timestamp))
	return jsonify(data=[i.serialize for i in window_log])
# show all the data from extended windows data
@api.route("/window_log/<window_id>/<page>")
def get_extended_window_data(window_id, page):
	window_log = Window.query.filter(Window.window_id == window_id).order_by(desc(Window.timestamp)).limit(30*int(page));
	return jsonify(data=[i.serialize for i in window_log])
@api.route("/window_index")
def get_all_window_data_index():
	from model import WindowIndex
	window_indexs = WindowIndex.query.all()
	return jsonify(data=[i.serialize for i in window_indexs])


@api.route("/notification", methods=['GET'])
def insert_notification():
	from model import Notification

	problem_id = request.args.get("problem_id", -1)
	gcm_id = request.args.get("gcm_id", -1)

	notification = Notification(problem_id, gcm_id)
	db.session.add(notification)
	db.session.commit()

	return jsonify(data=notification.id)

@api.route("/open_notification", methods=['GET'])
def update_open_notification():
	from model import Notification

	id = request.args.get("id", -1)

	indexs = db.session.query(Notification).filter_by(id=id).first()
	if indexs != None:
		indexs.open_timestamp = func.now()
		db.session.commit()
	return ""

@api.route("/response_notification", methods=['GET'])
def update_response_notification():
	from model import Notification

	id = request.args.get("id", -1)
	action = request.args.get("action", -1)
	annoy_level = request.args.get("annoy_level", -1)

	indexs = db.session.query(Notification).filter_by(id=id).first()
	if indexs != None:
		indexs.action = action
		indexs.annoy_level = annoy_level
		indexs.response_timestamp = func.now()

		db.session.commit()

	return ""

@api.route("/register_gcm_id", methods=['GET'])
def insert_gcm_id():
	from model import Member

	gcm_id = request.args.get("gcm_id", -1)
	index = db.session.query(Member).filter_by(gcm_id=gcm_id).first()

	if index != None:
		token = index.token
	else:
		member = Member(gcm_id=gcm_id)
		print jsonify(data=[member.serialize])
		db.session.add(member)
		db.session.commit()
		token = member.token

	return jsonify(token=token)

@api.route("/upload_wifi_signal", methods=['GET'])
def insert_wifi_signal():
	from model import WifiSignal

	location = request.args.get("location", -1)
	signal_level = request.args.get("signal_level", "")

	wifi_signal = WifiSignal(location, signal_level)
	db.session.add(wifi_signal)
	db.session.commit()

	return jsonify(data=[wifi_signal.serialize], success=1)

@api.route("/locations", methods=['GET'])
def get_locations():
	locations = Location.query.all()
	return jsonify(data=[i.serialize for i in locations])

@api.route("/window_action", methods=['GET'])
def window_action(): 

	token = request.args.get("token", -1)
	window_id = request.args.get("window_id", 0)
	action = request.args.get("action", -1)

	user = get_user_from_token(token)
	if user != None and window_id != 0 and action != -1:
		### query user id 
		hour = datetime.now(pytz.timezone('US/Pacific')).hour
		print hour
		if hour > 9 and hour < 20:
			action = int(action)
			if action == 0:
				feedback = insert_feedback(-1, 1, user_id, "positive", "get candy for closing window")
				return jsonify(status=1, reason=["close window for candies"], device_id=-1, user_id=user_id, application_id=feedback.application_id, feedback_id=feedback.feedback_id)
			elif action == 1: 
				return jsonify(status=0, reason=["no candy for opening window"]) 
			else:
				return jsonify(status=2, reason=["the action can't not be understanded"])
		elif hour <= 9 or hour>= 20:
			action = int(action)
			if action == 0: 
				return jsonify(status=0, reason=["no candy for closing window"])
			elif action == 1: 
				insert_feedback(-1, 1, user_id, "positive", "get candy for opening window")
				return jsonify(status=1, reason=["open window for candies"], device_id=-1, user_id=user_id, application_id=feedback.application_id, feedback_id=feedback.feedback_id)
				## good 
			else:
				return jsonify(status=2, reason=["the action can't not be understanded"])

@api.route("/people_around", methods=['GET'])
def people_around(): 
	#problem = Problem.query.filter(Problem.status == 0).first()
	device_id = request.args.get("device_id", -1)
	people_count = request.args.get("people_count", -1)
	if people_count == -1:
		return "suck"
	if device_id == -1:
		device_id = get_device_id_from_ip(request.remote_addr)
	if device_id == -1: 
		return "suck"

	data = json.load(urllib2.urlopen('http://cmu-sensor-network.herokuapp.com/lastest_readings_from_all_devices/light/json'))
	problems = []
	cleaned_data = []
	for row in data:
		firefly_time = datetime.fromtimestamp(row['timestamp']/1000).date()
		today_time = datetime.today().date()
		if today_time == firefly_time and row['device_id'] != "test" and row['device_id'] != "test-device" and row['device_id'] != "0":
			cleaned_data.append(row)
	for row in cleaned_data: 
		row_hour = datetime.fromtimestamp(row['timestamp']/1000).hour
		print datetime.fromtimestamp(row['timestamp']/1000).date(), row['device_id'], row['value']
		#if row['value'] > 1024 and mapping_table.has_key(row['device_id']) and (row_hour >= 21 or row_hour <= 7):
		#	problems.append(row)
		problems.append(row)
	if len(problems) > 0:
		problem_choosed = choice(problems)
		problem_repo_instance = None
		if problem_choosed != None:
			index = db.session.query(ProblemRepository).filter_by(valid=True).filter_by(device_feedback=device_id).first()
			if index != None:
				#index.problem_cat = "light"
				#index.problem_desc = "light is not closing now, could you help me to close it? I will give you candies if you do"
				#index.device_check = problem_choosed['device_id']
				#index.device_feedback = device_id
				#index.created_at = None 
				#index.location = mapping_table[problem_choosed['device_id']][2]
				#index.valid = True
				#problem_repo_instance = index
				#db.session.commit()
				return jsonify(problem=None)
			else:
				problem_repo_instance = ProblemRepository("light", "light is not closing now, could you help me to close it? I will give you candies if you do", mapping_table[problem_choosed['device_id']][2], problem_choosed['device_id'], device_id)
				db.session.add(problem_repo_instance)
				db.session.commit()
	else:
		return jsonify(problem=None)
	#return jsonify(data={"problem": problem.serialize})
	return jsonify(problem=problem_repo_instance.serialize)
@api.route("/get_problem", methods=['GET'])
def find_problem():
	device_id = request.args.get("device_id", -1)
	if device_id == -1: 
		device_id = get_device_id_from_ip(request.remote_addr)
	if device_id == -1:
		return jsonify(error=1)
	else: 
		index = db.session.query(ProblemRepository).filter_by(valid=True).filter_by(device_feedback=device_id).all()
		return jsonify(data=[i.serialize for i in index])

def loop_check_problem(): 
	#this function will loop in thread 
	start_time = time.time()
	while 1:
		import json 
		import urllib2
		print "check sensor repository..."
		problem_repos = db.session.query(ProblemRepository).filter_by(valid=True)
		data = json.load(urllib2.urlopen('http://cmu-sensor-network.herokuapp.com/lastest_readings_from_all_devices/light/json'))
		
		for p in problem_repos:
			#print p.serialize['device_check']
			for row in data:
				if row['device_id'] == str(p.serialize['device_check']):
					if row['value'] < 1023: 
						## did close the window! 
						print datetime.fromtimestamp(row['timestamp']/1000)
						print p.serialize['created_at']
						p.valid = False
						db.session.commit()
						delay_insert_feedback("", p.serialize['device_feedback'])
						print "give feedback to " + str(p.serialize['device_feedback'])
		#if problem_repos
		break;
	
	elapsed_time = time.time() - start_time
	print elapsed_time
	return 
mapping_table = {
"10170004": ["Firefly_v3","SensorAndrew0","B23.110"],
"10170202": ["Firefly_v3","SensorAndrew2","B23.216"],
"10170302": ["Firefly_v3","SensorAndrew3","B23.105B"],
"10170206": ["Firefly_v3","SensorAndrew2","B23.215B"],
"10170106": ["Firefly_v3","SensorAndrew1","B23.229"],
"10170306": ["Firefly_v3","SensorAndrew3","B23.124"],
"10170305": ["Firefly_v3","SensorAndrew3","B23.126"],
"10170002": ["Firefly_v3","SensorAndrew0","B23.115"],
"10170103": ["Firefly_v3","SensorAndrew1","B23.129"],
"10170303": ["Firefly_v3","SensorAndrew3","B23.104"],
"10170003": ["Firefly_v3","SensorAndrew0","B23.116"],
"10170102": ["Firefly_v3","SensorAndrew1","B23.129A"],
"10170104": ["Firefly_v3","SensorAndrew1","B23.230"],
"10170005": ["Firefly_v3","SensorAndrew0","B23.109"],
"10170307": ["Firefly_v3","SensorAndrew3","B23.122"],
"10170007": ["Firefly_v3","SensorAndrew0","B23.211"],
"10170304": ["Firefly_v3","SensorAndrew3","B23.123"],
"10170204": ["Firefly_v3","SensorAndrew2","B23.214"],
"10170203": ["Firefly_v3","SensorAndrew2","B23.213"],
"10170208": ["Firefly_v3","SensorAndrew2","B23.217A"],
"10170008": ["Firefly_v3","SensorAndrew0","B23.212"],
"10170009": ["Firefly_v3","SensorAndrew0","B23.210"],
"10170207": ["Firefly_v3","SensorAndrew2","B23.215"],
"10170308": ["Firefly_v3","SensorAndrew3","B23.120"],
"10170209": ["Firefly_v3","SensorAndrew2","B23.217B"],
"10170006": ["Firefly_v3","SensorAndrew0","B23.107"],
"10170205": ["Firefly_v3","SensorAndrew2","B23.214B"],
"10170105": ["Firefly_v3","SensorAndrew1","B23.228"]
}