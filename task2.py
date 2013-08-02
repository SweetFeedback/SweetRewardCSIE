from celery import Celery
import time
import json 
import urllib2
import config, os, sys	
path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sweet/')
sys.path.append(path)
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
		from model import *
		from feedbacks import *
		problem_repos = db.session.query(ProblemRepository).filter_by(valid=True)
		data = json.load(urllib2.urlopen('http://cmu-sensor-network.herokuapp.com/lastest_readings_from_all_devices/light/json'))
		print problem_repos
		for p in problem_repos:
			print p.serialize['device_check']
			for row in data:
				if row['device_id'] == str(p.serialize['device_check']):
					print row['value']
					if row['value'] < 300: 
						## did close the window! 
						print datetime.fromtimestamp(row['timestamp']/1000)
						print p.serialize['created_at']
						p.valid = False
						db.session.commit()
						#delay_insert_feedback("", p.serialize['device_feedback'])
						insert_feedback(p.serialize['device_feedback'], "10", -1, "positive", "you did close the light", can_get_time=None)
						print "give feedback to " + str(p.serialize['device_feedback'])
		#if problem_repos
		from model import *
		db.session.commit()
		break;
	elapsed_time = time.time() - start_time
	return elapsed_time 

if __name__ == "__main__" : 
	celery.worker_main()