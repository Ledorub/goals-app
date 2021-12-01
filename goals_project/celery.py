import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goals_project.settings')

app = Celery('goals_app')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()