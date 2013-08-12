from celery import Celery
import time
from datetime import datetime, timedelta
import json 
import urllib2
import config, os, sys	

path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sweet/')
sys.path.append(path)

from model import * 
celery = Celery("task2", 
				broker = 'redis://localhost:6379/0', 
				backend='redis')
celery.config_from_object('celeryconfig')

@celery.task(name = "task2.add")
def add(x, y):
	return x + y

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
						p.valid = False
						db.session.commit()
						#delay_insert_feedback("", p.serialize['device_feedback'])
						insert_feedback(p.serialize['device_feedback'], "10", -1, "positive", "you did close the light", can_get_time=15)
						print "give feedback to " + str(p.serialize['device_feedback'])
		#if problem_repos
		db.session.commit()
		break;
	elapsed_time = time.time() - start_time
	return elapsed_time 
@celery.task(name = "task2.noise_check")
def noise_check(): 
	start_time = time.time()

	online_machines = db.session.query(DeviceOnline).all()
	for machine in online_machines: 
		print "checking device " + machine.device_id
		machine_sensor_index = db.session.query(GumballSensorIndex).filter_by(device_id=machine.device_id).first()
		print machine_sensor_index.time
		noises = db.session.query(GumballSensor).filter(GumballSensor.time <= machine_sensor_index.time).filter(GumballSensor.time >= machine_sensor_index.time - timedelta(seconds=20))
		avr_noise_level = 0 
		#print "Get " + str(noises.count()) + " data to average"
		for n in noises:
			#print n.sound
			avr_noise_level = avr_noise_level + n.sound
		avr_noise_level = avr_noise_level / noises.count()
		#print avr_noise_level
		if machine_sensor_index != None and avr_noise_level >= 12:
			print "it's noisy here"
	db.session.commit()
	elapsed_time = time.time() - start_time
	return "used time for checking noise" + str(elapsed_time)
@celery.task(name = "task2.light_check")
def light_check():
	start_time = time.time()
	elapsed_time = time.time() - start_time
	## left for implementation 
	return "used time for checking light" + str(elapsed_time)
if __name__ == "__main__" : 
	celery.worker_main()