from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
if os.environ.get('DJANGO_SETTINGS_MODULE') is None:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.task_default_queue = 'default'
# app.task_routes = {
#     'core.tasks.google_sheet_export': {'queue': 'sheets'},
#     'core.tasks.verify_emails': {'queue': 'emails'},
# }
app.conf.beat_schedule = {
    'tasks-check-every-10': {
        'task': 'tasker.tasks.tasks_check',
        'schedule': 5.0,
        'options': {'queue': 'checks'}
    },
}
app.conf.timezone = 'UTC'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    import time
    time.sleep(30)
    print('Request: {0!r}'.format(self.request))