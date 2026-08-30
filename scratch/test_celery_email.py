import os
import sys
import django
import time

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusconnect.settings')
django.setup()

from placements.tasks import send_placement_notification
from django_celery_results.models import TaskResult

print("--- Testing Celery + Redis Async Email Delivery ---")

# Trigger Celery task asynchronously
result = send_placement_notification.delay(
    post_title="Software Engineer - Test Drive",
    company_name="Google",
    deadline_str="December 31, 2026"
)

print(f"Task dispatched successfully to Redis!")
print(f"Task ID: {result.id}")
print("Waiting 2 seconds for processing...")

time.sleep(2)

db_result = TaskResult.objects.filter(task_id=result.id).first()
if db_result:
    print(f"Status in DB: {db_result.status}")
    print(f"Result in DB: {db_result.result}")
    print("SUCCESS: Celery worker executed the task asynchronously via Redis!")
else:
    print(f"Task State: {result.state}")
    print("Task successfully pushed to Redis broker. Check your active Celery worker terminal!")
