from flask import Flask, Blueprint, render_template, request, jsonify, json
from celery import Celery 

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from sqlalchemy.sql import func
from model import *
from datetime import datetime, timedelta, date
import config, time, pytz, json, urllib2
from random import choice
from policyManager import *
from DBHelper import DBHelper

#blueprint
api = Blueprint('api', __name__)
db_helper = DBHelper()

@api.route("/application")
def get_applications(): 
	applications = db.session.query(Application).all()
	return jsonify(data=[i.serialize for i in applications])

@api.route("/application/register", methods=['GET'])
def register_application():
	app_name = request.args.get("application_name", "") 
	app_description = request.args.get("application_description", "")
	user_id = request.args.get("user_id", -1)

	application = Application(app_name, app_description, user_id)
	db.session.add(application)
	db.session.commit()

	return jsonify(data=[application.serialize])

@api.route("/online_device")
def get_online_device():
	online_device = db_helper.get_online_device()
	return jsonify(device=[i for i in online_device])


@api.route("/sensor_log_index/<device_id>")
def get_sensor_log(device_id):
	data = db_helper.get_sensor_index(device_id)
	return jsonify(data=[d.serialize for d in data])

@api.route("/sensor_log_index")
def get_all_sensor_log():
	data = db_helper.get_all_sensor_index()
	return jsonify(data=[d.serialize for d in data])

@api.route("/sensor_log/insert", methods=['GET'])
def sensor_insert():
	light_sensor = request.args.get("light_level", -1)
	sound_sensor = request.args.get("sound_level", -1)
	temp_sensor = request.args.get("temperature", -1)
	window_sensor = request.args.get("window_state", -1)
	device_id = request.args.get("device_id", -1)
	
	if device_id != -1:
		db_helper.device_login_or_update(device_id, request.remote_addr)
	else: 
		return jsonify(error="it's needed to provide device id.")
	if light_sensor != -1:
		db_helper.insert_light(device_id, light_sensor, "gumball machine")
	if sound_sensor != -1:
		db_helper.insert_sound(device_id, sound_sensor, "gumball machine")
	if temp_sensor != -1:
		db_helper.insert_temperature(device_id, temp_sensor, "gumball machine")	
	if window_sensor != -1:
		db_helper.insert_window(device_id, window_sensor, "gumball machine")
	return jsonify(success=1)






@api.route("/locations", methods=['GET'])
def get_locations():
	locations = Location.query.all()
	return jsonify(data=[i.serialize for i in locations])



@api.route("/people_around", methods=['GET'])
def people_around(): 
	#problem = Problem.query.filter(Problem.status == 0).first()
	device_id = request.args.get("device_id", -1)
	people_count = request.args.get("people_count", -1)
	if people_count == -1:
		return "suck"
	if device_id == -1:
		device_id = db_helper.get_device_id_from_ip(request.remote_addr)
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
		if row['value'] > 500 and mapping_table.has_key(row['device_id']) and (row_hour >= 21 or row_hour <= 7):
			problems.append(row)
		#problems.append(row)
	if len(problems) > 0:
		problem_choosed = choice(problems)
		problem_repo_instance = None
		if problem_choosed != None:
			index = db.session.query(ProblemRepository).filter_by(valid=True).filter_by(device_feedback=device_id).first()
			if index != None:
				index.problem_cat = "light"
				index.problem_desc = "light is not closing now, could you help me to close it? I will give you candies if you do"
				index.device_check = problem_choosed['device_id']
				index.device_feedback = device_id
				index.created_at = None 
				index.location = mapping_table[problem_choosed['device_id']][2]
				index.valid = True
				problem_repo_instance = index
				db.session.commit()
			#	return jsonify(problem=None)
			else:
				problem_repo_instance = ProblemRepository("light", "light is not closing now, could you help me to close it? I will give you candies if you do", mapping_table[problem_choosed['device_id']][2], problem_choosed['device_id'], device_id)
				db.session.add(problem_repo_instance)
				db.session.commit()
	else:
		return jsonify(problem=None)
	#return jsonify(data={"problem": problem.serialize})
	return jsonify(problem=problem_repo_instance.serialize)

@api.route("/confirm_to_solve_problem", methods=['GET'])
def confirm_to_solve_problem():
	problem_id = request.args.get("problem_id", -1)
	if problem_id != -1: 
		problem_in_repository = db.session.query(ProblemRepository).filter_by(problem_id=problem_id).first()
		if problem_in_repository != None: 
			problem_in_repository.valid = True
			return jsonify(update=problem_in_repository.serialize)
	return jsonify(error="Non-existed problem.")
@api.route("/get_problem", methods=['GET'])
def find_problem():
	device_id = request.args.get("device_id", -1)
	if device_id == -1: 
		device_id = db_helper.get_device_id_from_ip(request.remote_addr)
	if device_id == -1:
		return jsonify(error=1)
	else: 
		index = db.session.query(ProblemRepository).filter_by(valid=True).filter_by(solved=False).filter_by(device_feedback=device_id).all()
		if len(index) == 0:
			return jsonify(data={"problem":[], "question":get_one_random_question().serialize})
		return jsonify(data={"problem":[i.serialize for i in index], "question":[]})

@api.route("/questionnaire")
def show_question():
	questions = db.session.query(QuestionRepository).all()
	return render_template("quiz.html", q=get_random_questions(questions))
def get_random_questions(questions):
	random_questions = [] 
	indexs = range(len(questions))

	index = choice(indexs)
	random_questions.append(questions[index])
	indexs.pop(indexs.index(index))

	index = choice(indexs)
	random_questions.append(questions[index])
	indexs.pop(indexs.index(index))

	index = choice(indexs)
	random_questions.append(questions[index])
	indexs.pop(indexs.index(index))
	return random_questions
def get_one_random_question():
	questions = db.session.query(QuestionRepository).all()
	random_one = None

	indexs = range(len(questions))
	index = choice(indexs)
	random_one = questions[index]
	#indexs.pop(indexs.index(index))
	return random_one


@api.route("/feedbacks/<application_id>/<years>/<months>/<days>")
def get_feedbacks(years, months, days, application_id):
	feedbacks = get_list_feedbacks(int(years), int(months), int(days), int(application_id))
	return jsonify(data=[i.serialize for i in feedbacks])
def get_list_feedbacks(y, m, d, a):
	day_datetime = datetime.fromordinal(date(y, m, d).toordinal())
	next_day_datetime = datetime.fromordinal((date(y, m, d)+ timedelta(days=1)).toordinal())
	feedbacks = Feedback.query.filter_by(application_id=a).filter(Feedback.created_time < next_day_datetime).filter(Feedback.created_time > day_datetime).all()
	return feedbacks

@api.route("/feedbacks/leaderboard/device")
def get_feedbacks_leaderboard_device():
	feedbacks = db.session.query(Feedback.device_id, func.count(Feedback.device_id)).group_by(Feedback.device_id).order_by(desc(func.count(Feedback.device_id))).all()
	return jsonify(data=[{"device_id": i[0], "count": i[1]} for i in feedbacks]) 
@api.route("/feedbacks/leaderboard/user")
def get_feedbacks_leaderboard_user():
	feedbacks = db.session.query(Feedback.user_id, func.count(Feedback.user_id)).filter(Feedback.user_id != -1).group_by(Feedback.user_id).order_by(desc(func.count(Feedback.user_id))).all()
	return jsonify(data=[{"user_id": i[0], "count": i[1]} for i in feedbacks])
@api.route("/feedbacks/leaderboard/application_id")
def get_feedbacks_leaderboard_application():
	feedbacks = db.session.query(Feedback.application_id, func.count(Feedback.application_id)).filter(Feedback.application_id != -1).group_by(Feedback.application_id).order_by(desc(func.count(Feedback.application_id))).all()
	return jsonify(data=[{"application_id": i[0], "count": i[1]} for i in feedbacks])

@api.route("/feedback_insert", methods=['GET'])
def feedback_insert():
	device_id = request.args.get("device_id", -1)
	application_id = request.args.get("application_id", -1)
	user_id = request.args.get("user_id", -1)
	feedback_type = request.args.get("feedback_type", -1)
	feedback_description = request.args.get("feedback_description", "")	
	can_get_time = request.args.get("can_get_time", 0)

	time = datetime.now()
	if can_get_time != 0:
		time = datetime.now() + timedelta(seconds=int(can_get_time))
	
	if device_id == -1:
		device_id = db_helper.get_device_id_from_ip(request.remote_addr)
	if db_helper.insert_feedback(device_id, application_id, user_id, feedback_type, feedback_description) is True:
		return jsonify(success="1")
	return jsonify(error="1")

@api.route("/get_feedback", methods=['GET'])
def feedback():
	device_id = request.args.get("device_id", -1)
	feedbacks = Feedback.query.filter_by(device_id=device_id).filter_by(if_get=False).filter(Feedback.can_get_time <= datetime.now()).all()
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
	user = get_user_from_token(token)
	feedbacks = Feedback.query.filter_by(user_id=user.user_id).filter_by(if_get=False).filter(Feedback.can_get_time < datetime.now())
	return jsonify(data=[i.serialize for i in feedbacks])
@api.route("/update_feedback", methods=['GET'])
def update_feedback():
	feedback_id = request.args.get("feedback_id", -1)
	feedback = db.session.query(Feedback).filter_by(feedback_id=feedback_id).first()
	if feedback is not None:
		feedback.if_get = True
		feedback.retrieve_time = datetime.now()
		db.session.commit()
	return jsonify(data=[feedback.serialize])
