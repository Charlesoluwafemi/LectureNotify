from celery import Celery
from celery.schedules import crontab
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lecture_notify.settings')
app = Celery('lecture_notify')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Define the schedule for sending notifications
app.conf.beat_schedule = {
    'send_notifications_before_lecture': {
        'task': 'backend.tasks.send_whatsapp_notification_to_students',
        'schedule': crontab(hour=3, minute=33), 
       
    },
}

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()



