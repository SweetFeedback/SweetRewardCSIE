from model import *
from task2 import insert_sensor
from task2 import insert_feedback_task
class DBHelper:
	def __init__(self):
		self.fuck = 1 

	def get_online_device(self):
		online_devices = [] 
		database_object = DeviceOnline.query.all()
		if database_object.count > 0:
			for obj in database_object:
				online_devices.append(obj.serialize)
		return online_devices
	

	def insert_question_log(self, problem_id, via_device, option, correct): 
		question_record = QuestionLog(problem_id, via_device, option, correct)
		db.session.add(question_record)
		db.session.commit()
		return question_record
	def insert_feedback(self, device_id, app_id, user_id, feedback_type, feedback_desc, can_get_time=None):
		insert_feedback_task.apply_async((device_id, app_id, user_id, feedback_type, feedback_desc, can_get_time))
		return True
	def update_feedback(self, feedback_id):
		if feedback_id != -1:
			feedback = db.session.query(Feedback).filter_by(feedback_id=feedback_id).first()
			if feedback is not None:
				feedback.if_get = True
				feedback.retrieve_time = datetime.now()
				db.session.commit()
		return True
	def get_feedback(self, device_id):
		feedbacks = Feedback.query.filter_by(device_id=device_id).filter_by(if_get=False).filter(Feedback.can_get_time <= datetime.now()).all()
		return feedbacks

	### sensors related ### 
	def insert_light(self, device_id, sensor_value, module_type):
		insert_sensor.apply_async((device_id, "light", module_type, sensor_value))
		return True
	
	def insert_sound(self, device_id, sensor_value, module_type, sensor_index=1):
		insert_sensor.apply_async((device_id, "sound", module_type, sensor_value, sensor_index))
		return True
	
	def insert_temperature(self, device_id, sensor_value, module_type, sensor_index=1):
		insert_sensor.apply_async((device_id, "temperature", module_type, sensor_value, sensor_index))
		return True
	
	def insert_window(self, device_id, sensor_value, module_type, sensor_index=1):
		insert_sensor.apply_async((device_id, "window", module_type, sensor_value, sensor_index))

	def insert_people(self, device_id, sensor_value, module_type, sensor_index=1):
		insert_sensor.apply_async((device_id, "people", module_type, sensor_value, sensor_index))

	def insert_survey(self, data):
		survey = SurveyLog(data)
		print survey
		db.session.add(survey)
		db.session.commit()
		return True
	
	def get_sensor_index(self, device_id):
		sensor_log_indexs = db.session.query(SensorIndex).filter_by(device_id=device_id).all()
		for i in sensor_log_indexs:
			print i.serialize
		return sensor_log_indexs
	def get_sensor_index_by_type(self, sensor_type):
		sensor_log_indexs = db.session.query(SensorIndex).filter_by(sensor_type=sensor_type).all()
		#for i in sensor_log_indexs:
			#print i.serialize
		return sensor_log_indexs
	def get_all_sensor_index(self):
		online_devices = self.get_online_device()
		all_sensor_index = [] 
		for device in online_devices:
			all_sensor_index.extend(self.get_sensor_index(device['device_id']))
		return all_sensor_index
	def get_user_from_token(self, token):
		if token is not None and token != "":
			user = db.session.query(Member).filter_by(token=token).first()
			if user is not None:
				return user
		return None
	
	def get_user_from_fb(self, facebook_id):
		if facebook_id is not None and facebook_id != "":
			user = db.session.query(Member).filter_by(facebook_id=facebook_id).first()
			if user is not None:
				return user
		return None
	
	def get_user_from_account(self, account):
		if account is not None and account != "":
			user = db.session.query(Member).filter_by(account=account).first()
			if user is not None:
				return user
		return None
	
	def get_user_from_gcm_id(self, gcm_id):
		if gcm_id is not None and gcm_id != "": 
			user = db.session.query(Member).filter_by(gcm_id=gcm_id).first() 
			if user is not None: 
				return user
		return None
	
	def get_user_from_bluetooth_id(self, bluetooth_id):
		if bluetooth_id is not None and bluetooth_id != "": 
			user = db.session.query(Member).filter_by(bluetooth_id=bluetooth_id).first() 
			if user is not None: 
				return user
		return None
	def get_device_id_from_ip(self, address):
		device_id = -1
		device_status = db.session.query(DeviceOnline).filter_by(ipaddress=address).first()
		if device_status is not None: 
			device_id = device_status.device_id
		return device_id

	def device_login_or_update(self, device_id, address):
		self.check_online_device()
		device_status = db.session.query(DeviceOnline).filter_by(device_id=device_id).first()

		if device_status is not None:
			device_status.time = datetime.now()
			device_status.ipaddress = address
			db.session.commit()
		else:
			timestamp = datetime.now()
			device_status = DeviceOnline(device_id, timestamp, address)
			db.session.add(device_status)
			db.session.commit()
		return device_status
	def check_online_device(self):
		devices = DeviceOnline.query.all()
		now = datetime.now()
		device_delete = []
		for device in devices: 
			diff =  (now - device.time).seconds / 60
			if diff > 1: ## 10 mins 
				db.session.delete(device)
				db.session.commit()
				device_delete.append(device)
		return device_delete
	def get_device_id_from_ip(self, address):
		device_id = -1
		device_status = db.session.query(DeviceOnline).filter_by(ipaddress=address).first()
		if device_status is not None: 
			device_id = device_status.device_id
		return device_id