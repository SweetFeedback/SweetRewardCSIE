from celery.schedules import crontab
from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'task2.check',
        'schedule': timedelta(seconds=15),
        'args': (),
    },
    'every-15-seconds-for-noise': {
    	'task' : 'task2.find_noise',
    	'schedule' : timedelta(seconds=15),
    	'args': ()
    },
    'every-15-seconds-for-checking-noise': {
    	'task': 'task2.check_noise',
    	'schedule': timedelta(seconds=15),
    	'args': () 
    }
}
