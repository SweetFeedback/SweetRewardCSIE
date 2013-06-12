from flask import Flask, Blueprint, render_template, request, jsonify, json
from celery import Celery 
from tasks import add

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from sqlalchemy.sql import func
from model import app, db, Problem, Feedback
import config

#blueprint
api = Blueprint('api', __name__)

@api.route("/reports")
def show_reports():
	problems = Problem.query.all()
	return jsonify(data=[i.serialize for i in problems])

@api.route("/reports/solved")
def show_reports_unsolved():
	problems = Problem.query.filter(Problem.status == 0).all()
	return jsonify(data=[i.serialize for i in problems])

@api.route("/reports/unsolved")
def show_reports_unsolved():
	problems = Problem.query.filter(Problem.status == 1).all()
	return jsonify(data=[i.serialize for i in problems])

@api.route("/reports/location/<room_id>")
def show_reports_room(room_id):
	problems = Problem.query.filter(Problem.room_id == room_id).all()
	return jsonify(data=[i.serialize for i in problems])

@api.route("/reports/insert", methods=['GET', 'POST'])
def insert_report():
	title = request.args.get("title", "")
	content = request.args.get("content", "")
	coor_x = request.args.get("coor_x", 0)
	coor_y = request.args.get("coor_y", 0)
	user_id = request.args.get("user_id", 0)
	category = request.args.get("category", 0)
	room_id = request.args.get("room_id", 0)

	report = Problem(category, room_id, title, content, coor_x, coor_y, user_id)
	db.session.add(report)
	db.session.commit()

	return jsonify(data=[report.serialize], success=1)

@api.route("/reports/update/<report_id>", methods=['GET', 'POST'])
def update_report(report_id):	
	user_id = request.args.get("user_id", 0)
	target_problem = Problem.query.filter_by(problem_id = report_id).first()
	if target_problem is not None:
		target_problem.status = 1
		target_problem.updated_by = user_id
		db.session.commit()
		return_result = jsonify(data=[target_problem.serialize])
	else:
		return_result = jsonify(error=["can't find this problem from database"])
	return return_result

@api.route("/members")
def list_members():
	from model import Member
	members = Member.query.all()
	return jsonify(data=[i.serialize for i in members])

# going to insert window_log data 
@api.route("/window_log/insert", methods=['GET', 'POST'])
def insert_window_log():
	from model import Window, WindowIndex
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
		indexs.state = window_log.state
		indexs.timestamp = window_log.timestamp
		db.session.commit()
		print "update records"
	
	print location_id, window_id, state
	return ""
# show all the data from extended windows data
@api.route("/window_log")
def get_all_extended_window_data():
	from model import Window
	window_log = Window.query.filter(Window.window_id == 1).order_by(desc(Window.timestamp)).all();
	#print window_log.log_id
	#for i in range(len(window_log)):
	#	print window_log[i].log_id
	#print window_log
	#return " " + str(window_log.log_id) + " " +  str(window_log.state) + " " +str(window_log.timestamp)
	return jsonify(data=[i.serialize for i in window_log])
@api.route("/window_index")
def get_window_data_index():
	from model import WindowIndex
	window_indexs = WindowIndex.query.all()
	return jsonify(data=[i.serialize for i in window_indexs])


@api.route("/feedbacks")
def get_all_feedback_record():
	feedbacks = Feedback.query.all()
	return jsonify(data=[i.serialize for i in feedbacks])

@api.route("/notification", methods=['GET'])
def insert_notification():
	from model import Notification

	problem_id = request.args.get("problem_id", -1)
	gcm_id = request.args.get("gcm_id", -1)

	notification = Notification(problem_id, gcm_id)
	db.session.add(notification)
	db.session.commit()

	return ""

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
	from model import GcmID

	gcm_id = request.args.get("gcm_id", -1)
	user_id = request.args.get("user_id", -1)

	gcm = GcmID(gcm_id, user_id)
	if user_id == -1:
		db.session.add(gcm)
		db.session.commit()
	else:
		indexs = db.session.query(GcmID).filter_by(gcm_id=gcm_id).first()
		if indexs != None:
			indexs.user_id = gcm.user_id
			db.session.commit()

	return ""
