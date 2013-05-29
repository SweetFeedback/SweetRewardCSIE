from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP
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
		self.status = 0
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
	__tablename__ = "extended_window_log2"

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



