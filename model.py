from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Table, Column, Text, Integer, String, Date, Float, TIMESTAMP, BOOLEAN
import config
import md5

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
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

	def __init__(self, problem_cat, problem_desc, location, device_check, device_feedback):
		self.problem_desc = problem_desc
		self.problem_cat = problem_cat
		self.location = location 
		self.valid = 1
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
			'valid' : self.valid
		}
	def __repr__(self):
		return "problem_repository"


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

class WifiSignal(db.Model):
	__tablename__ = "wifi_signal"

	id = db.Column("id", Integer, primary_key=True)
	location = db.Column("location", Integer)
	signal_level = db.Column("signal_level", Text)
	timestamp = db.Column("timestamp", TIMESTAMP)

	def __init__(self, location, signal_level):
		self.location = location
		self.signal_level = signal_level

	@property
	def serialize(self):
		return {
			'id': self.id,
			'location': self.location,
			'signal_level': self.signal_level,
			'timestamp': str(self.timestamp)
		}
	def __repr__(self):
		return "WifiSignal"

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
class GumballSensor(db.Model):
	__tablename__ = "basic_sensor_log"
	log_id = db.Column("log_id", Integer, primary_key=True)
	device_id = db.Column("device_id", Integer)
	light = db.Column("light_level", Float) 
	temperature = db.Column("temperature", Float)
	sound = db.Column("sound_level", Float)
	time = db.Column("created_time", TIMESTAMP)

	def __init__(self, device_id, light, temp, sound):
		self.device_id = device_id
		self.light = light
		self.temperature = temp
		self.sound = sound
	@property
	def serialize(self):
		return { 
			'log_id' : self.log_id,
			'device_id' : self.device_id,
			'light_level' : self.light,
			'temperature' : self.temperature,
			'sound_level' : self.sound,
			'created_at' : str(self.time)
		}
	def __repr__(self):
		return "Sensor log " + str(self.log_id) + " "  + str(self.device_id) + "(" + str(light) + "," + str(temperature) + "," + str(sound) + ")"
class GumballSensorIndex(db.Model):
	__tablename__ = "basic_sensor_log_index"
	log_id = db.Column("log_id", Integer, primary_key=True)
	sensor_log_id = db.Column("sensor_log_id", Integer)
	device_id = db.Column("device_id", Integer)
	light = db.Column("light_level", Float) 
	temperature = db.Column("temperature", Float)
	sound = db.Column("sound_level", Float)
	time = db.Column("created_time", TIMESTAMP)

	def __init__(self, sensor_log_id, device_id, light, temp, sound):
		self.sensor_log_id = sensor_log_id
		self.device_id = device_id
		self.light = light
		self.temperature = temp
		self.sound = sound
	@property
	def serialize(self):
		return { 
			'log_id' : self.log_id,
			'sensor_log_id' : self.sensor_log_id,
			'device_id' : self.device_id,
			'light_level' : self.light,
			'temperature' : self.temperature,
			'sound_level' : self.sound,
			'created_at' : str(self.time)
		}
	def __repr__(self):
		return "Sensor log index" + str(self.log_id) + " " + str(self.sensor_log_id) + " " + str(self.device_id) + "(" + str(self.light) + "," + str(self.temperature) + "," + str(self.sound) + ")"

class DeviceAround(db.Model):
	__tablename__ = "device_around"

	log_id = db.Column("log_id", Integer, primary_key=True)
	nearby_device = db.Column("nearby_device", Integer)
	bluetooth_id = db.Column("bluetooth_id", String(50))
	device_name = db.Column("device_name", String(50))
	timestamp = db.Column("timestamp", TIMESTAMP)

	def __init__(self, nearby_device, bluetooth_id, device_name):
		self.nearby_device = nearby_device
		self.bluetooth_id = bluetooth_id
		self.device_name = device_name
	@property
	def serialize(self):
		return {
			'log_id' : self.log_id,
			'nearby_device' : self.nearby_device,
			'bluetooth_id' : self.bluetooth_id,
			'device_name' : self.device_name,
			'timestamp' : self.timestamp
		}
	def __repr__(self):
		return "Device Around log " + str(self.log_id) + " :" + self.nearby_device + ", (" + str(self.bluetooth_id) + ", " + str(self.device_name) + ") at" + str(self.timestamp)
