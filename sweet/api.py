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
	if device_id == -1:
		device_id = db_helper.get_device_id_from_ip(request.remote_addr)
	
	if people_count != -1 and device_id != -1:
		db_helper.insert_people(device_id, people_count, "macintosh")
	sentences = [{"sentence": "Hey! I saw you.", "tone": "Whisper"}, {"sentence" : "I got you guys", "tone": "Vicki"}, {"sentence": "Hey! guys !", "tone": "Albert"}, {"sentence": "Don't go", "tone": "Albert"}]
	sentence_choosen = choice(sentences)
	return jsonify(words=sentence_choosen)

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
		current_time = datetime.now() - timedelta(minutes=10)
		index = db.session.query(ProblemRepository).filter_by(valid=False).filter_by(solved=False).filter_by(device_feedback=device_id).filter(ProblemRepository.created_at > current_time).all()
		if index.count == 0:
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
	if device_id == -1: 
		device_id = db_helper.get_device_id_from_ip(request.remote_addr)
	feedbacks = db_helper.get_feedback(device_id)
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
	db_helper.update_feedback(feedback_id)
	return ""

@api.route("/question_log", methods=['GET'])
def question_log () : 
	problem_id = request.args.get("problem_id", -1)
	option = request.args.get("option", -1 )
	correct = request.args.get("correct", 0)
	device_id = request.args.get("device_id", -1)
	question_record = None
	
	if device_id == -1:
		device_id = db_helper.get_device_id_from_ip(request.remote_addr)
	if int(correct) == 1 and problem_id != -1 and option != -1: 
		db_helper.insert_feedback(device_id, 9, -1, "saying", "you got right answer")
		db_helper.insert_question_log(problem_id, device_id, option, 1)

	elif int(correct) == 0 and problem_id != -1 and option != -1:
		db_helper.insert_feedback(device_id, 9, -1, "saying", "you got wrong answer")
		db_helper.insert_question_log(problem_id, device_id, option, 0)

	return jsonify(data=question_record.serialize)

@api.route("/upload_survey", methods=['POST'])
def upload_survey():
	print request.form
	question1 = request.form.getlist('question1')
	question2 = request.form.getlist('question2')
	question3 = request.form.getlist('question3')
	question4 = request.form.getlist('question4')
	#question3 = request.form.getlist('question3[]')
	#question4 = request.form.getlist('question4[]')
	question5 = request.form.getlist('question5')
	question6 = request.form.getlist('question6')
	question7 = request.form.getlist('question7')
	question8 = request.form.getlist('question8')
	question9 = request.form.getlist('question9')
	question10 = request.form.getlist('question10')
	question11 = request.form.getlist('question11')

	'''
	'question3_1': True if '1' in question3 else False,
		'question3_2': True if '2' in question3 else False,
		'question3_3': True if '3' in question3 else False,
		'question3_4': True if '4' in question3 else False,
		'question3_5': True if '5' in question3 else False,
		'question3_6': True if '6' in question3 else False,
		'question3_7': True if '7' in question3 else False,
		'question4_1': True if '1' in question4 else False,
		'question4_2': True if '2' in question4 else False,
		'question4_3': True if '3' in question4 else False,
		'question4_4': True if '4' in question4 else False,
		'question4_5': True if '5' in question4 else False,
		'question4_6': True if '6' in question4 else False,
		'question4_7': True if '7' in question4 else False,
	'''

	print question1
	print question2
	print question3
	print question4
	print question5
	print question6
	print question7
	print question8
	print question9
	print question10
	print question11


	data = {
		'question1': -1 if len(question1) == 0 else int(question1[0]),
		'question2': -1 if len(question2) == 0 else int(question2[0]),
		'question3': -1 if len(question3) == 0 else int(question3[0]),
		'question4': -1 if len(question4) == 0 else int(question4[0]),
		'question5': -1 if len(question5) == 0 else int(question5[0]),
		'question6': -1 if len(question6) == 0 else int(question6[0]),
		'question7': -1 if len(question7) == 0 else int(question7[0]),
		'question8': -1 if len(question8) == 0 else int(question8[0]),
		'question9': -1 if len(question9) == 0 else int(question9[0]),
		'question10': -1 if len(question10) == 0 else int(question10[0]),
		'question11': -1 if len(question11) == 0 else question11[0]
	}
	db_helper.insert_survey(data)

	return "";


