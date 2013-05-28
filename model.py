from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP
from database import Base
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
db = SQLAlchemy(app)


class Member(Base):
	__tablename__ = "members"

	user_id = Column("user_id", Integer, primary_key=True)
	account = Column("account", String(65) )
	password = Column("password", String(65))
	token = Column("token", String(65))
	temp = Column("temperature_threshold", Float)
	light = Column("light_threshold", Float)
	micro = Column("micro_threshold", Float)

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

class Problem(Base):
	__tablename__ = "problems"

	problem_id = Column("id", Integer, primary_key=True)
	category_id = Column("category", Integer)
	room_id = Column("room", Integer)
	title = Column("title", String(255))
	description = Column("description", String(255))
	coor_x = Column("coordinate_x", Integer)	
	coor_y = Column("coordinate_y", Integer)
	created_by_id = Column("created_by", Integer)
	status = Column("status", Integer)
	created_at = Column("created_at", TIMESTAMP)
	updated_at = Column("updated_at", TIMESTAMP)
	updated_by = Column("updated_by", Integer)

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


class Online(Base):
	__tablename__ = "user_online"

	user_id = Column("user_id", Integer, primary_key=True)
	time = Column("time", Integer)
	ipaddr = Column("ipaddr", String(50))

	def __repr__(self):
		return 'online'

class Window(Base):
	__tablename__ = "extended_window_log2"

	log_id = Column("ext_win_log_id", Integer, primary_key=True)
	location_id = Column("location_id", Integer)
	window_id = Column("window_id", Integer)
	state = Column("state", Integer)
	timestamp = Column("timestamp", TIMESTAMP)
	
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
class WindowIndex(Base):
	__tablename__ = "extended_window_log_index"

	index_id = Column("log_id", Integer, primary_key=True)
	log_id = Column("ext_win_log_id", Integer)
	location_id = Column("location_id", Integer)
	window_id = Column("window_id", Integer)
	state = Column("state", Integer)
	timestamp = Column("timestamp", TIMESTAMP)

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



