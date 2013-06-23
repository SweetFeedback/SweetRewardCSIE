from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Table, Column, Text, Integer, String, Date, Float, TIMESTAMP, BOOLEAN
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
db = SQLAlchemy(app)


class Member(db.Model):
	__tablename__ = "members"

	user_id = db.Column("user_id", Integer, primary_key=True)
	account = db.Column("account", String(65) )
	password = db.Column("password", String(65))
	token = db.Column("token", String(65))
	temp = db.Column("temperature_threshold", Float)
	light = db.Column("light_threshold", Float)
	micro = db.Column("micro_threshold", Float)

	@property
	def serialize(self):
		return {
			'user_id' : self.user_id,
			'account' : self.account,
			'token' : self.token,
			'temp_threshold' : self.temp,
			'light_threshold' : self.light,
			'micro_threshold' : self.micro
		}	

	def __repr__(self):
		return '<sweetfeedback member user_id:%d account:%r threshold:%8.1f %8.1f %8.1f' % (self.user_id, self.account, self.temp, self.light, self.micro)

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

	def __init__(self, category_id=None, room_id=None, title=None, description=None, coordinate_x=None, coordinate_y=None, created_by=None):
		self.category_id = category_id
		self.room_id = room_id
		self.title = title
		self.description = description
		self.coor_x = coordinate_x
		self.coor_y = coordinate_y
		self.created_by_id = created_by
		self.status = 1
		self.created_at = datetime.utcnow()

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


class Online(db.Model):
	__tablename__ = "user_online"

	user_id = db.Column("user_id", Integer, primary_key=True)
	time = db.Column("time", Integer)
	ipaddr = db.Column("ipaddr", String(50))

	def __repr__(self):
		return 'online'

class Window(db.Model):
	__tablename__ = "extended_window_log"

	log_id = db.Column("ext_win_log_id", Integer, primary_key=True)
	location_id = db.Column("location_id", Integer)
	window_id = db.Column("window_id", Integer)
	state = db.Column("state", Integer)
	timestamp = db.Column("timestamp", TIMESTAMP)
	
	def __init__(self, location_id=None, window_id=None, state=None):
		self.location_id = location_id
		self.window_id = window_id
		self.state = state
	
	@property 
	def serialize(self):
		return {
			'log_id' : self.log_id,
			'location_id' : self.location_id,
			'window_id' : self.window_id,
			'state' : self.state,
			'timestamp' : str(self.timestamp)
		}
	def __repr__(self):
		return '<extended window sensor data location:%d window:%d state:%d>' % (self.location_id, self.window_id, self.state)
class WindowIndex(db.Model):
	__tablename__ = "extended_window_log_index"

	index_id = db.Column("log_id", Integer, primary_key=True)
	log_id = db.Column("ext_win_log_id", Integer)
	location_id = db.Column("location_id", Integer)
	window_id = db.Column("window_id", Integer)
	state = db.Column("state", Integer)
	timestamp = db.Column("timestamp", TIMESTAMP)

	def __init__ (self, log_id, location_id, window_id, state, timestamp):
		self.log_id = log_id
		self.location_id = location_id
		self.window_id = window_id
		self.state = state	
		self.timestamp = timestamp	

	@property 
	def serialize(self):
		return {
			'index_id' : self.index_id,
			'log_id' : self.log_id,
			'location_id' : self.location_id,
			'window_id' : self.window_id,
			'state' : self.state,
			'timestamp' : str(self.timestamp)
		}
	def __repr__(self):
		return 'window index'

class Feedback(db.Model):
	__tablename__ = "feedback_repository"
	feedback_id = db.Column("feedback_id", Integer, primary_key=True)
	device_id = db.Column("device_id", Integer)
	application_id = db.Column("application_id", Integer)
	user_id = db.Column("user_id", Integer)
	feedback_type = db.Column("feedback_type", String(50))
	feedback_description = db.Column("feedback_description", String(200))
	created_time = db.Column("created_time", TIMESTAMP)
	if_get = db.Column("if_get", BOOLEAN)

	def __init__ (self, device_id, application_id, user_id, feedback_type, feedback_description):
		self.device_id = device_id
		self.application_id = application_id
		self.user_id = user_id
		self.feedback_type = feedback_type
		self.feedback_description = feedback_description
		self.created_time = datetime.utcnow()
		self.if_get = False

	@property
	def serialize(self):
		return {
			'feedback_id' : self.feedback_id,
			'device_id' : self.device_id,
			'application_id' : self.application_id,
			'user_id' : self.user_id,
			'feedback_type': self.feedback_type,
			'feedback_description': self.feedback_description,
			'created_time' : str(self.created_time),
			'if_get' : self.if_get
		}
	def __repr__(self):
		return "feedback record"

class Notification(db.Model):
	__tablename__ = "notification"

	id = db.Column("id", Integer, primary_key=True)
	problem_id = db.Column("problem_id", Integer)
	gcm_id = db.Column("gcm_id", Text)
	action = db.Column("action", Integer)
	annoy_level = db.Column("annoy_level", Integer)
	open_timestamp = db.Column("open_timestamp", Integer)
	response_timestamp = db.Column("response_timestamp", Integer)
	generate_timestamp = db.Column("generate_timestamp", TIMESTAMP)

	def __init__ (self, problem_id, gcm_id):
		self.problem_id = problem_id
		self.gcm_id = gcm_id


	@property
	def serialize(self):
		return {
			'id': self.id,
			'problem_id': self.problem_id,
			'gcm_id': self.gcm_id,
			'action': self.action,
			'annoy_level': self.annoy_level,
			'open_timestamp': self.open_timestamp,
			'response_timestamp': self.response_timestamp,
			'generate_timestamp': self.generate_timestamp
		}
	def __repr__(self):
		return "Notification"

class GcmID(db.Model):
	__tablename__ = "gcm_id"

	id = db.Column("id", Integer, primary_key=True)
	gcm_id = db.Column("gcm_id", Integer)
	user_id = db.Column("user_id", Integer)
	timestamp = db.Column("timestamp", TIMESTAMP)

	def __init__ (self, gcm_id, user_id):
		self.gcm_id = gcm_id
		self.user_id = user_id

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'gcm_id' : self.gcm_id,
			'user_id' : self.user_id,
			'timestamp': self.timestamp
		}
	def __repr__(self):
		return "RegisterGCMID"
