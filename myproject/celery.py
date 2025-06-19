import os
from celery import Celery

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from myapp.tasks import sample_task
app.conf.beat_schedule = {
    'sample-task-every-10-seconds': {
        'task': 'myapp.tasks.sample_task',
        'schedule': 10.0,  # Run every 10 seconds
    },
}
app.conf.timezone = 'Asia/Kolkata'