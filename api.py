from flask import Flask, Blueprint, render_template, request, jsonify, json
from celery import Celery 
from tasks import add

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from sqlalchemy.sql import func
from model import app, db, Problem, Feedback, Member, Window, Location, WindowIndex, DeviceOnline, GumballSensor, GumballSensorIndex
import config
from members import *
from datetime import datetime 
import pytz
#blueprint
api = Blueprint('api', __name__)
@api.route("/sensor_log/insert", methods=['GET'])
def sensor_insert():
	light_sensor = request.args.get("light_level", -1)
	sound_sensor = request.args.get("sound_level", -1)
	temp_sensor = request.args.get("temperature", -1)
	device_id = request.args.get("device_id", -1)
	
	if device_id != -1:
		device_login_or_update(device_id, request.remote_addr)

	sensor_log = GumballSensor(device_id, light_sensor, temp_sensor, sound_sensor)
	db.session.add(sensor_log)
	db.session.commit()

	# insert to window index table 	
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
	
	return jsonify(data=[sensor_log.serialize])
@api.route("/test", methods=['GET'])
def test(): 
	status = device_login_or_update(get_device_id_from_ip(request.remote_addr), request.remote_addr)
	return jsonify(address=status.serialize)
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
		if diff > 10: ## 10 mins 
			#device_delete.append(device)
			db.session.delete(device)
			db.session.commit()
	return ""
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

### method related to feedback 
@api.route("/feedbacks")
def get_all_feedback_record():
	feedbacks = Feedback.query.all()
	return jsonify(data=[i.serialize for i in feedbacks])
@api.route("/feedback_insert", methods=['GET'])
def feedback_insert():
	device_id = request.args.get("device_id", -1)
	application_id = request.args.get("application_id", -1)
	user_id = request.args.get("user_id", -1)
	feedback_type = request.args.get("feedback_type", -1)
	feedback_description = request.args.get("feedback_description", "")	
	if device_id == -1:
		device_id = get_device_id_from_ip(request.remote_addr)
	return insert_feedback(device_id, application_id, user_id, feedback_type, feedback_description)
	
def insert_feedback(device_id, app_id, user_id, feedback_type, feedback_desc):
	feedback = Feedback(device_id, app_id, user_id, feedback_type, feedback_desc)
	db.session.add(feedback)
	db.session.commit()
	return jsonify(data=feedback.serialize)

@api.route("/get_feedback", methods=['GET'])
def feedback():
	device_id = request.args.get("device_id", -1)
	feedbacks = Feedback.query.filter_by(device_id=device_id).filter_by(if_get=False)
	return jsonify(data=[i.serialize for i in feedbacks])

@api.route("/retrieve_feedback", methods=['GET'])
def retrieve_feedback():
	device_id = request.args.get("device_id", -1)
	feedback_id = request.args.get("feedback_id", -1)
	user_id = request.args.get("user_id", -1)
	feedback = Feedback.query.filter_by(feedback_id=feedback_id).first()
	if feedback is not None: 
		feedback.device_id = device_id
		db.session.commit()
	return jsonify(data=[feedback.serialize])
@api.route("/get_feedback_by_user", methods=['GET'])
def get_feedback_by_user():
	token = request.args.get("token", -1)
	user_id = get_id_from_token(token)
	feedbacks = Feedback.query.filter_by(user_id=user_id).filter_by(if_get=False)
	return jsonify(data=[i.serialize for i in feedbacks])
@api.route("/update_feedback", methods=['GET'])
def update_feedback():
	feedback_id = request.args.get("feedback_id", -1)
	feedback = db.session.query(Feedback).filter_by(feedback_id=feedback_id).first()
	if feedback is not None:
		feedback.if_get = True
		db.session.commit()
	return jsonify(data=[feedback.serialize])

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

	user_id = get_id_from_token(token)
	if user_id != 0 and window_id != 0 and action != -1:
		### query user id 
		hour = datetime.now(pytz.timezone('US/Pacific')).hour
		print hour
		if hour > 9 and hour < 20:
			action = int(action)
			if action == 0:
				insert_feedback(100, 1, user_id, "positive", "get candy for closing window")
				return jsonify(status=1, reason=["close window for candies"], device_id=0, user_id=1, application_id=1, feedback_id=1)
			elif action == 1: 
				return jsonify(status=0, reason=["no candy for opening window"]) 
			else:
				return jsonify(status=2, reason=["the action can't not be understanded"])
		elif hour <= 9 or hour>= 20:
			action = int(action)
			if action == 0: 
				return jsonify(status=0, reason=["no candy for closing window"])
			elif action == 1: 
				insert_feedback(100, 1, user_id, "positive", "get candy for opening window")
				return jsonify(status=1, reason=["open window for candies"], device_id=0, user_id=1, application_id=1, feedback_id=1)
				## good 
			else:
				return jsonify(status=2, reason=["the action can't not be understanded"])
