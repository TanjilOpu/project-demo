import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seminar_library.settings')

app = Celery('seminar_library')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Run reminder check every day at 8 AM
app.conf.beat_schedule = {
    'send-due-reminders-daily': {
        'task': 'notifications.tasks.send_due_reminders',
        'schedule': crontab(hour=8, minute=0),
    },
}
