from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import os, sys
from sqlalchemy import Table, Column, Text, Integer, String, Date, Float, TIMESTAMP, BOOLEAN

import md5

app = Flask(__name__, template_folder = "../templates", static_folder= "../static")
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


class Member(db.Model):
	__tablename__ = "members"

	user_id = db.Column("user_id", Integer, primary_key=True)
	account = db.Column("account", String(65))
	password = db.Column("password", String(65))
	nickname = db.Column("nickname", String(50))
	token = db.Column("token", String(65))
	temp = db.Column("temperature_threshold", Float)
	light = db.Column("light_threshold", Float)
	micro = db.Column("micro_threshold", Float)
	facebook_id = db.Column("facebook_id", Text)
	gcm_id = db.Column("gcm_id", Text)
	bluetooth_id = db.Column("bluetooth_id", Text)

	def __init__(self, account=None, password=None, nickname=None, token=None, temp=0, light=0, micro=0, facebook_id=None, gcm_id=None, bluetooth_id=None):
		self.account = account
		self.password = password
		self.nickname = nickname
		self.temp = temp
		self.light = light
		self.micro = micro
		self.facebook_id = facebook_id
		self.gcm_id = gcm_id
		self.bluetooth_id = bluetooth_id
		self.token = token
		if account != None:
			self.token = md5.new(account).hexdigest()
		elif gcm_id != None:
			self.token = md5.new(gcm_id).hexdigest()
		elif facebook_id != None:
			self.token = md5.new(facebook_id).hexdigest()
		elif bluetooth_id != None:
			self.token = md5.new(bluetooth_id).hexdigest()

	@property
	def serialize(self):
		return {
			'user_id' : self.user_id,
			'account' : self.account,
			'nickname' : self.nickname,
			'token' : self.token,
			'temp_threshold' : self.temp,
			'light_threshold' : self.light,
			'micro_threshold' : self.micro,
			'facebook_id' : self.facebook_id,
			'gcm_id' : self.gcm_id,
			'bluetooth_id' : self.bluetooth_id
		}	

	def __repr__(self):
		return '<sweetfeedback member user_id:%d account:%s nickname:%sthreshold:%8.1f %8.1f %8.1f' % (self.user_id, self.account, self.nickname, self.temp, self.light, self.micro)

class Problem(db.Model):
	__tablename__ = "problems"

	problem_id = db.Column("id", Integer, primary_key=True)
	category_id = db.Column("category", Integer)
	room_id = db.Column("room", Integer)
	title = db.Column("title", String(255))
	description = db.Column("description", String(255))
	coor_x = db.Column("coordinate_x", Integer)	
	coor_y = db.Column("coordinate_y", Integer)
	created_by_id = db.Column("created_by", Integer)
	status = db.Column("status", Integer)
	created_at = db.Column("created_at", TIMESTAMP)
	updated_at = db.Column("updated_at", TIMESTAMP)
	updated_by = db.Column("updated_by", Integer)

	def __init__(self, category_id=None, room_id=None, title=None, description=None, coordinate_x=None, coordinate_y=None):
		self.category_id = category_id
		self.room_id = room_id
		self.title = title
		self.description = description
		self.coor_x = coordinate_x
		self.coor_y = coordinate_y
		self.created_by_id = created_by
		self.status = 0

	@property
	def serialize(self):
		return {
			'problem_id' : self.problem_id,
			'category_id' : self.category_id,
			'room_id' : self.room_id,
			'title' : self.title,
			'description' : self.description,
			'coordinate_x' : self.coor_x,
			'coordinate_y' : self.coor_y,
			'created_by' : self.created_by_id,
			'status' : self.status,
			'created_at' : str(self.created_at),
			'updated_at' : str(self.updated_at),
			'updated_by' : self.updated_by
		}
	def __repr__(self):
		return "problem"

class ProblemRepository(db.Model):
	__tablename__ = "problem_repository"

	problem_id = db.Column("problem_id", Integer, primary_key=True)
	problem_cat = db.Column("problem_cat", String(50))
	problem_desc = db.Column("problem_desc", String(200))
	location = db.Column("location", String(50))
	device_check = db.Column("device_check", Integer)
	device_feedback = db.Column("device_feedback", Integer)
	created_at = db.Column("created_at", TIMESTAMP)
	valid = db.Column("valid", BOOLEAN)
	solved = db.Column("solved", BOOLEAN)

	def __init__(self, problem_cat, problem_desc, location, device_check, device_feedback, valid=0):
		self.problem_desc = problem_desc
		self.problem_cat = problem_cat
		self.location = location 
		self.valid = valid
		self.device_check = device_check
		self.device_feedback = device_feedback

	@property
	def serialize(self): 
		return {
			'problem_id' : self.problem_id, 
			'problem_cat' : self.problem_cat, 
			'problem_desc' : self.problem_desc, 
			'location' : self.location,
			'device_check' : self.device_check,
			'device_feedback' : self.device_feedback,
			'created_at' : self.created_at,
			'valid' : self.valid,
			'solved' : self.solved

		}
	def __repr__(self):
		return "problem_repository"

class Feedback(db.Model):
	__tablename__ = "feedback_repository"
	feedback_id = db.Column("feedback_id", Integer, primary_key=True)
	device_id = db.Column("device_id", Integer)
	application_id = db.Column("application_id", Integer)
	user_id = db.Column("user_id", Integer)
	feedback_type = db.Column("feedback_type", String(50))
	feedback_description = db.Column("feedback_description", String(200))
	can_get_time = db.Column("can_get_time", TIMESTAMP)
	retrieve_time = db.Column("retrieve_time", TIMESTAMP)
	created_time = db.Column("created_time", TIMESTAMP)
	if_get = db.Column("if_get", BOOLEAN)

	def __init__ (self, device_id, application_id, user_id, feedback_type, feedback_description, can_get_time=None):
		self.device_id = device_id
		self.application_id = application_id
		self.user_id = user_id
		self.feedback_type = feedback_type
		self.feedback_description = feedback_description
		self.created_time = datetime.now()
		self.if_get = False
		if can_get_time is not None:
			self.can_get_time = can_get_time
		else:
			self.can_get_time = datetime.now()

	@property
	def serialize(self):
		return {
			'feedback_id' : self.feedback_id,
			'device_id' : self.device_id,
			'application_id' : self.application_id,
			'user_id' : self.user_id,
			'feedback_type': self.feedback_type,
			'feedback_description': self.feedback_description,
			'can_get_time' : str(self.can_get_time),
			'retrieve_time' : str(self.retrieve_time),
			'created_time' : str(self.created_time),
			'if_get' : self.if_get
		}
	def __repr__(self):
		return "feedback record"

class Location(db.Model):
	__tablename__ = "Locations"

	id = db.Column("location_id", Integer, primary_key=True)
	name = db.Column("room_name", String(50))
	coordinate_x = db.Column("coordinate_x", Integer)
	coordinate_y = db.Column("coordinate_y", Integer)
	floor_level = db.Column("floor_level", Integer)

	def __init__(self, name, x, y, floor_level):
		self.name = name
		self.floor_level = floor_level
		self.coordinate_x = x
		self.coordinate_y = y

	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'floor_level': self.floor_level,
			'coordinate_x': self.coordinate_x,
			'coordinate_y': self.coordinate_y
		}
	def __repr__(self):
		return "Location"

class DeviceOnline(db.Model):
	__tablename__ = "device_online"

	device_id = db.Column("session", Integer, primary_key=True)
	time = db.Column("time",TIMESTAMP)
	ipaddress = db.Column("ipaddress", String(50))

	def __init__(self, device_id, time, ipaddress):
		self.device_id = device_id
		self.time = time 
		self.ipaddress = ipaddress
	@property
	def serialize(self):
		return { 
			'device_id': self.device_id,
			'time': str(self.time),
			'ipaddress': self.ipaddress
		}
	def __repr__(self):
		return "Online machine " + str(self.device_id) + " from " + str(self.time)
class Application(db.Model):
	__tablename__ = "applications"

	application_id = db.Column("application_id", Integer, primary_key=True)
	name = db.Column("name", String(50))
	description = db.Column("description", String(200))
	owner_id = db.Column("owner_id", Integer)
	created_at = db.Column("created_at", TIMESTAMP)

	def __init__ (self, name, description, owner_id):
		self.name = name
		self.description = description
		self.owner_id = owner_id

	@property
	def serialize(self):
		return {
			'application_id' : self.application_id,
			'name' : self.name, 
			'description' : self.description,
			'owner_id' : self.owner_id,
			'created_at' : self.created_at
		}

	def __repr__(self):
		return "Application"

class QuestionRepository(db.Model):
	__tablename__ = "question_repository"

	problem_id = db.Column("problem_id", Integer, primary_key=True)
	problem_desc = db.Column("problem_desc", String(200))
	problem_category = db.Column("category", String(50))
	option_1 = db.Column("option_1", String(50))
	option_2 = db.Column("option_2", String(50))
	option_3 = db.Column("option_3", String(50))
	option_4 = db.Column("option_4", String(50))
	error_message = db.Column("error_message", String(200))
	answer = db.Column("answer", Integer)
	updated_at = db.Column("updated_at", TIMESTAMP)

	def __init__(self, desc, cat, o_1, o_2, o_3, o_4, error_message, ans):
		self.problem_desc = desc
		self.problem_category = cat
		self.option_1 = o_1
		self.option_2 = o_2
		self.option_3 = o_3
		self.option_4 = o_4
		self.error_message = error_message
		self.answer = ans

	@property
	def serialize(self):
		return { 
			'problem_id' : self.problem_id,
			'problem_desc' : self.problem_desc,
			'problem_category' : self.problem_category,
			'option_1' : self.option_1,
			'option_2' : self.option_2,
			'option_3' : self.option_3, 
			'option_4' : self.option_4,
			'answer' : self.answer,
			'error_message' : self.error_message,
			'updated_at' : self.updated_at
		}
	def __repr__(self):
		return "question_repository" + str(self.problem_id) + ", " + str(self.problem_desc) + ", "  + str(self.problem_category)
class Sensor(db.Model):
	__tablename__ = "sensors"

	log_id = db.Column("log_id", Integer, primary_key=True)
	sensor_type = db.Column("sensor_type", String(20))
	module_type = db.Column("module_type", String(50))
	sensor_index = db.Column("sensor_index", Integer)
	sensor_value = db.Column("sensor_value", Integer)
	created_at = db.Column("created_at", TIMESTAMP)
	device_id = db.Column("device_id", Integer)

	def __init__(self, sensor_type, module_type, sensor_value, device_id, sensor_index=1):
		self.sensor_type = sensor_type
		self.module_type = module_type
		self.sensor_index = sensor_index
		self.sensor_value = sensor_value
		self.device_id = device_id

	@property
	def serialize(self):
		return {
			'log_id' : self.log_id,
			'sensor_type' : self.sensor_type,
			'module_type' : self.module_type,
			'sensor_index' : self.sensor_index,
			'device_id' : self.device_id,
			'sensor_value' : self.sensor_value,
			'created_at' : self.created_at
		}
	def __repr__(self):
		return "sensor " + str(self.log_id) + " type " + self.sensor_type + " from " + self.module_type + " value:" + str(self.sensor_value)

class SensorIndex(db.Model):
	__tablename__ = "sensors_index"

	log_id = db.Column("log_id", Integer, primary_key=True)
	sensor_type = db.Column("sensor_type", String(20))
	module_type = db.Column("module_type", String(50))
	sensor_index = db.Column("sensor_index", Integer)
	sensor_value = db.Column("sensor_value", Integer)
	created_at = db.Column("created_at", TIMESTAMP)
	device_id = db.Column("device_id", Integer)

	def __init__(self, sensor_type, module_type, sensor_value, device_id, sensor_index=1):
		self.sensor_type = sensor_type
		self.module_type = module_type
		self.sensor_index = sensor_index
		self.sensor_value = sensor_value
		self.device_id = device_id

	@property
	def serialize(self):
		return { 
			'log_id' : self.log_id,
			'sensor_type' : self.sensor_type,
			'module_type' : self.module_type,
			'sensor_index' : self.sensor_index,
			'device_id' : self.device_id,
			'sensor_value' : self.sensor_value,
			'created_at' : self.created_at
		}
	def __repr__(self):
		return "Sensor Index" + str(self.log_id) + " type " + self.sensor_type + " from " + self.module_type + " value:" + str(self.sensor_value)
class QuestionLog(db.Model):
	__tablename__ = "question_log"

	log_id = db.Column("log_id", Integer, primary_key=True)
	problem_id = db.Column("problem_id", Integer)
	answer = db.Column("answer", Integer)
	correct = db.Column("correct", BOOLEAN)
	created_at = db.Column("created_at", TIMESTAMP)

	def __init__ (self, problem_id, answer, correct):
		self.problem_id = problem_id
		self.answer = answer
		self.correct = correct

	@property
	def serialize(self):
		return { 
			'log_id' : self.log_id,
			'problem_id' : self.problem_id,
			'answer' : self.answer,
			'correct' : self.correct,
			'created_at' : self.created_at
		}
	def __repr__(self):
		return "question log " + self.problem_id + ", " + self.answer + ", " + self.correct+ " " + self.created_at

class SurveyLog(db.Model):
	__tablename__ = "survey_log"

	survey_id = db.Column("survey_id", Integer, primary_key=True)
	question1 = db.Column("question1", Integer)
	question2 = db.Column("question2", Integer)
	question3 = db.Column("question3", Integer)
	question4 = db.Column("question4", Integer)
	'''
	question3_1 = db.Column("question3_1", BOOLEAN)
	question3_2 = db.Column("question3_2", BOOLEAN)
	question3_3 = db.Column("question3_3", BOOLEAN)
	question3_4 = db.Column("question3_4", BOOLEAN)
	question3_5 = db.Column("question3_5", BOOLEAN)
	question3_6 = db.Column("question3_6", BOOLEAN)
	question3_7 = db.Column("question3_7", BOOLEAN)
	question4_1 = db.Column("question4_1", BOOLEAN)
	question4_2 = db.Column("question4_2", BOOLEAN)
	question4_3 = db.Column("question4_3", BOOLEAN)
	question4_4 = db.Column("question4_4", BOOLEAN)
	question4_5 = db.Column("question4_5", BOOLEAN)
	question4_6 = db.Column("question4_6", BOOLEAN)
	question4_7 = db.Column("question4_7", BOOLEAN)
	'''
	question5 = db.Column("question5", Integer)
	question6 = db.Column("question6", Integer)
	question7 = db.Column("question7", Integer)
	question8 = db.Column("question8", Integer)
	question9 = db.Column("question9", Integer)
	question10 = db.Column("question10", Integer)
	question11 = db.Column("question11", String(255))
	created_at = db.Column("created_at", TIMESTAMP)

	def __init__(self, data):
		self.question1 = data['question1']
		self.question2 = data['question2']
		self.question3 = data['question3']
		self.question4 = data['question4']
		'''
		self.question3_1 = data['question3_1']
		self.question3_2 = data['question3_2']
		self.question3_3 = data['question3_3']
		self.question3_4 = data['question3_4']
		self.question3_5 = data['question3_5']
		self.question3_6 = data['question3_6']
		self.question3_7 = data['question3_7']
		self.question4_1 = data['question4_1']
		self.question4_2 = data['question4_2']
		self.question4_3 = data['question4_3']
		self.question4_4 = data['question4_4']
		self.question4_5 = data['question4_5']
		self.question4_6 = data['question4_6']
		self.question4_7 = data['question4_7']
		'''
		self.question5 = data['question5']
		self.question6 = data['question6']
		self.question7 = data['question7']
		self.question8 = data['question8']
		self.question9 = data['question9']
		self.question10 = data['question10']
		self.question11 = data['question11']

		print self.question1
		print self.question2
		print self.question3
		print self.question4
		print self.question5
		print self.question6
		print self.question7
		print self.question8
		print self.question9
		print self.question10
		print self.question11

