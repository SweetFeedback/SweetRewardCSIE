from celery.schedules import crontab
from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'task2.check',
        'schedule': timedelta(seconds=15),
        'args': (),
    },
    'every-30seconds-for-noise': {
    	'task' : 'task2.noise_check',
    	'schedule' : timedelta(seconds=30),
    	'args': ()
    }
}
