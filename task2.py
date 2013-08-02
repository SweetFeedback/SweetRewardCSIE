from celery import Celery

celery = Celery("task2", 
				broker = 'redis://localhost:6379/0', 
				backend='redis')
celery.config_from_object('celeryconfig')

@celery.task(name = "task2.add")
def add(x, y):
	return x + y

@celery.task(name = "task2.check")
def check(): 
	i = 30;
	while i > 0:
		i = i - 1
	return True

if __name__ == "__main__" : 
	celery.worker_main()