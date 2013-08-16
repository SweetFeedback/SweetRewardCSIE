from model import *
from task2 import add 
from task2 import insert_sensor
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
		return True
	def insert_feedback(self, device_id, app_id, user_id, feedback_type, feedback_desc, can_get_time=None):
		add.apply_async((device_id, app_id, user_id, feedback_type, feedback_desc, can_get_time))
		return True
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

