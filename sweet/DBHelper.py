from model import *
from task2 import add 
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

	def insert_data(self, device_id, app_id, user_id, feedback_type, feedback_desc, can_get_time=None):
		add.apply_async((device_id, app_id, user_id, feedback_type, feedback_desc, can_get_time))
		return "done"
	def insert_feedback(self, device_id, app_id, user_id, feedback_type, feedback_desc, can_get_time=None):
		add.apply_async((device_id, app_id, user_id, feedback_type, feedback_desc, can_get_time))
		return True