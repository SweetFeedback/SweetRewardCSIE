from flask import Flask, Blueprint, render_template, request, jsonify, json
from celery import Celery 
from tasks import add

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from sqlalchemy.sql import func
from model import app, db, Problem, Feedback, Member, Window, Location
import config

from datetime import datetime 
import pytz
#blueprint
api = Blueprint('api', __name__)

### function related to members 
@api.route("/members")
def list_members():
	members = Member.query.all()
	return jsonify(data=[i.serialize for i in members])

# going to insert window_log data 
@api.route("/window_log/insert", methods=['GET', 'POST'])
def insert_window_log():
	location_id = request.args.get("location_id", -1)
	window_id = request.args.get("window_id", -1)
	state = request.args.get("state", -1)

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
		print "update records"
	
	print location_id, window_id, state
	return jsonify(data=[window_log.serialize])

@api.route("/window_log")
def get_all_extended_window_data():
	window_log = Window.query.filter(Window.window_id == 1).order_by(desc(Window.timestamp))
	return jsonify(data=[i.serialize for i in window_log])
# show all the data from extended windows data
@api.route("/window_log/<page>")
def get_extended_window_data(page):
	window_log = Window.query.filter(Window.window_id == 1).order_by(desc(Window.timestamp)).limit(30*int(page));
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
	return insert_feedback(device_id, application_id, user_id, feedback_type, feedback_description)
	
def insert_feedback(device_id, app_id, user_id, feedback_type, feedback_desc):
	feedback = Feedback(device_id, app_id, user_id, feedback_type, feedback_desc)
	db.session.add(feedback)
	db.session.commit()
	return jsonify(data=feedback.serialize)


@api.route("/get_feedback", methods=['GET'])
def feedback():
	device_id = request.args.get("device_id", "-1")
	feedbacks = Feedback.query.filter_by(device_id=device_id).filter_by(if_get=False)
	return jsonify(data=[i.serialize for i in feedbacks])
@api.route("/get_feedback_by_user", methods=['GET'])
def get_feedback_by_user():
	user_id = request.args.get("user_id", -1)
	feedbacks = Feedback.query.filter_by(user_id=user_id).filter_by(if_get=False)
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
	return jsonify(data=[i.serialize for i in locations], success=1)

@api.route("/window_action", methods=['GET'])
def window_action(): 

	token = request.args.get("token", -1)
	window_id = request.args.get("window_id", 0)
	action = request.args.get("action", -1)

	if token != -1 and window_id != 0 and action != -1:
		### query user id 
		mdatetime = datetime.now(pytz.timezone('US/Pacific')).hour

		if hour > 9 and hour < 20:
			if action == 0:
				## good 
				insert_feedback(device_id, application_id, user_id, feedback_type, feedback_description)
				return jsonify(getcandy=["close window"])
			elif action == 1: 
				## bad
				print ""
		elif hour <= 9 and hour>= 20:
			if action == 0: 
				## bad
				print ""
			elif action == 1: 
				insert_feedback(device_id, application_id, user_id, feedback_type, feedback_description)
				return jsonify(getcandy=["open window"])
				## good 
				
		### check if the action is good 
