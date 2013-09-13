from celery import Celery
import time
from datetime import datetime, timedelta
import json 
import urllib2
import config, os, sys	

path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sweet/')
sys.path.append(path)

#from api import *
from model import * 
from policyManager import *

celery = Celery("task2", 
				broker = 'redis://localhost:6379/0', 
				backend='redis')
celery.config_from_object('celeryconfig')

@celery.task(name = "task2.insert_feedback")
def insert_feedback_task(device_id, app_id, user_id, feedback_type, feedback_desc, can_get_time=None):
	feedback = Feedback(device_id, app_id, user_id, feedback_type, feedback_desc, can_get_time)
	db.session.add(feedback)
	db.session.commit()
	return feedback

@celery.task(name = "task2.insert_sensor")
def insert_sensor(device_id, sensor_type, module_type, sensor_value, sensor_index=1):
	insert_sensor_repository(device_id, sensor_type, module_type, sensor_value, sensor_index)
	insert_sensor_index(device_id, sensor_type, module_type, sensor_value, sensor_index)
	return True

def insert_sensor_repository(device_id, sensor_type, module_type, sensor_value, sensor_index=1):
	sensor_log = Sensor(sensor_type, module_type, sensor_value, device_id, sensor_index)
	db.session.add(sensor_log)
	db.session.commit()
	return sensor_log
def insert_sensor_index(device_id, sensor_type, module_type, sensor_value, sensor_index=1):
	sensor_index_record = db.session.query(SensorIndex).filter_by(device_id=device_id).filter_by(sensor_type=sensor_type).filter_by(module_type=module_type).filter_by(sensor_index=sensor_index).first()
	if sensor_index_record != None:
		sensor_index_record.sensor_value = sensor_value
		db.session.commit()
	else:
		sensor_index_record = SensorIndex(sensor_type, module_type, sensor_value, device_id, sensor_index)
		db.session.add(sensor_index_record)
		db.session.commit()
	return sensor_index_record

@celery.task(name = "task2.check")
def check(): 
	return loop_check_problem()

def loop_check_problem(): 
	#this function will loop in thread 
	start_time = time.time()
	while 1:
		print "check sensor repository..."
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sweet/')
		sys.path.append(path)
		problem_repos = db.session.query(ProblemRepository).filter_by(valid=True)
		data = json.load(urllib2.urlopen('http://cmu-sensor-network.herokuapp.com/lastest_readings_from_all_devices/light/json'))
		print problem_repos
		for p in problem_repos:
			print p.serialize['device_check']
			for row in data:
				if row['device_id'] == str(p.serialize['device_check']):
					print row['value']
					if row['value'] < 1024: 
						## did close the window! 
						print datetime.fromtimestamp(row['timestamp']/1000)
						print p.serialize['created_at']
						p.solved = True
						db.session.commit()
						#delay_insert_feedback("", p.serialize['device_feedback'])
						insert_feedback(p.serialize['device_feedback'], "10", -1, "positive", "you did close the light", can_get_time=15)
						print "give feedback to " + str(p.serialize['device_feedback'])
		#if problem_repos
		db.session.commit()
		break;
	elapsed_time = time.time() - start_time
	return elapsed_time 
@celery.task(name = "task2.find_noise")
def find_noise(): 
	start_time = time.time()

	online_machines = db.session.query(DeviceOnline).all()
	for machine in online_machines: 
		print "checking device " + machine.device_id
		machine_sensor_index = db.session.query(GumballSensorIndex).filter_by(device_id=machine.device_id).first()
		print machine_sensor_index.time
		noises = db.session.query(GumballSensor).filter_by(device_id=machine.device_id).filter(GumballSensor.time <= machine_sensor_index.time).filter(GumballSensor.time >= machine_sensor_index.time - timedelta(seconds=15))
		avr_noise_level = 0 
		#print "Get " + str(noises.count()) + " data to average"
		for n in noises:
			#print n.sound
			avr_noise_level = avr_noise_level + n.sound
		avr_noise_level = avr_noise_level / noises.count()
		print "average noise level is " + str(avr_noise_level)
		if machine_sensor_index != None and isNoisy(avr_noise_level) is True:
			insert_noise_problem_to_problem_repository(machine_sensor_index.device_id)
			print "it's noisy here"
	elapsed_time = time.time() - start_time
	return "used time for finding noise " + str(elapsed_time)
@celery.task(name="task2.check_noise")
def check_noise():
	start_time = time.time()
	print "check local sensor repository for noise..."
	
	problem_repos = db.session.query(ProblemRepository).filter_by(valid=True).filter_by(solved=False).filter_by(problem_cat="noise")
	for p in problem_repos:
		machine_sensor_index = db.session.query(GumballSensorIndex).filter_by(device_id=p.device_check).first()
		noises = db.session.query(GumballSensor).filter_by(device_id=p.device_check).filter(GumballSensor.time <= machine_sensor_index.time).filter(GumballSensor.time >= machine_sensor_index.time - timedelta(seconds=15))
		avr_noise_level = 0 
		#print "Get " + str(noises.count()) + " data to average"
		for n in noises:
			#print n.sound
			avr_noise_level = avr_noise_level + n.sound
		avr_noise_level = avr_noise_level / noises.count()
		print "average noise level is " + str(avr_noise_level)
		if machine_sensor_index != None and isNoisy(avr_noise_level) is not True:
			p.solved = True
			p.valid = False
			db.session.commit()
			insert_feedback(p.device_feedback, "13", -1, "positive", "Thank you for lowering noise.", can_get_time=5)
			print "it's not that noisy now"

	elapsed_time = time.time() - start_time
	return "used time for checking noise " + str(elapsed_time)

@celery.task(name = "task2.find_light")
def find_light(): 
	start_time = time.time() 
	elapsed_time = time.time() - start_time
	sensor_log_indexs = db.session.query(SensorIndex).filter_by(sensor_type="light").all()
	#for i in sensor_log_indexs:
		#print i.serialize
	for i in sensor_log_indexs:
		print i.sensor_value
		date_object = datetime.strptime(i.created_at, '%b %d %Y %I:%M%p')
		if i.sensor_value > 200 and (date_object.hour >= 21 or date_object.hour <= 7): 
			problem_repo_instance = ProblemRepository("light", "light is not closing now, could you help me to close it? I will give you candies if you do", "gumball machine" + str(i.device_id), i.device_id, i.device_id)
	'''data = json.load(urllib2.urlopen('http://cmu-sensor-network.herokuapp.com/lastest_readings_from_all_devices/light/json'))
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
		if row['value'] < 700 and mapping_table.has_key(row['device_id']) and (row_hour >= 21 or row_hour <= 7):
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
				index.valid = False
				problem_repo_instance = index
				db.session.commit()
			#	return jsonify(problem=None)
			else:
				problem_repo_instance = ProblemRepository("light", "light is not closing now, could you help me to close it? I will give you candies if you do", mapping_table[problem_choosed['device_id']][2], problem_choosed['device_id'], device_id)
				db.session.add(problem_repo_instance)
				db.session.commit()
	'''
	return "used time for finding light " + str(elapsed_time)
@celery.task(name = "task2.light_check")
def light_check():
	start_time = time.time()	
	print "check sensor repository..."
	
	problem_repos = db.session.query(ProblemRepository).filter_by(valid=True).filter_by(solved=False).filter_by(problem_cat="light")
	
	data = json.load(urllib2.urlopen('http://cmu-sensor-network.herokuapp.com/lastest_readings_from_all_devices/light/json'))
	for p in problem_repos:
		print p.serialize['device_check']
		for row in data:
			if row['device_id'] == str(p.serialize['device_check']):
				print row['value']
				if isLightNormal(row['value']) is True: 
					p.valid = False
					p.solved = True
					db.session.commit()
					insert_feedback(p.serialize['device_feedback'], "10", -1, "positive", "you did close the light", can_get_time=15)
					print "give feedback to " + str(p.serialize['device_feedback'])
	#if problem_repos
	db.session.commit()
	elapsed_time = time.time() - start_time
	## left for implementation 

	return "used time for checking light " + str(elapsed_time)
### problem repository 
def insert_noise_problem_to_problem_repository(device_id):
	problem_repo_instance = ProblemRepository("Noise", "Is is noisy here?", "Device " + str(device_id), device_id, device_id, valid=True)
	db.session.add(problem_repo_instance)
	db.session.commit()
def insert_light_problem_to_problem_repository(firefly_id, device_id):
	problem_repo_instance = ProblemRepository("light", "light is not closing now, could you help me to close it? I will give you candies if you do", mapping_table[firefly_id][2], firefly_id, device_id)
	db.session.add(problem_repo_instance)
	db.session.commit()
if __name__ == "__main__" : 
	celery.worker_main()