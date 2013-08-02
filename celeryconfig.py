from celery.schedules import crontab
from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'task2.check',
        'schedule': timedelta(seconds=15),
        'args': (),
    },
}