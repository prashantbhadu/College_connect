"""
Celery application for CampusConnect.

This module is imported by campusconnect/__init__.py so the Celery app is
always ready before Django starts processing requests.
"""

import os
from celery import Celery

# Tell Celery which Django settings module to use.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusconnect.settings')

app = Celery('campusconnect')

# Pull Celery config from Django settings — any key starting with CELERY_ is used.
app.config_from_object('django.conf:settings', namespace='CELERY')
# --- FIX: Tell Celery to retry connecting to Redis on startup ---
app.conf.broker_connection_retry_on_startup = True 
# Automatically discover tasks.py in every installed app.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Utility task — run `celery call campusconnect.celery.debug_task` to verify worker."""
    print(f'Request: {self.request!r}')
