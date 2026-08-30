"""
Celery tasks for the placements app.

Replaces the old daemon-thread approach in utils.py with a proper async task:
  - Retries automatically up to 3 times on any exception (60 s back-off).
  - Result stored in the Django DB via django_celery_results.
  - Visible in Celery Flower / `celery inspect` for monitoring.
"""

import logging
from celery import shared_task
from django.core.mail import send_mass_mail
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=60,        # wait 60 s, then 120 s, then 240 s before each retry
    max_retries=3,
    default_retry_delay=60,
    acks_late=True,          # only acknowledge the task after it completes (safe on worker crash)
)
def send_placement_notification(self, post_title: str, company_name: str, deadline_str: str):
    """
    Send a placement notification email to every active student.

    Arguments are plain JSON-serialisable types (no Django model instances)
    because Celery serialises task args to JSON before passing them to the worker.

    Args:
        post_title:    The role/title of the placement post.
        company_name:  Name of the hiring company.
        deadline_str:  Pre-formatted deadline string, e.g. "September 15, 2026".
    """
    from accounts.models import UserProfile

    students = (
        UserProfile.objects
        .filter(user_type='student')
        .exclude(email__isnull=True)
        .exclude(email='')
    )

    if not students.exists():
        logger.info('[placement_notification] No student emails found — skipping.')
        return

    from_email = (
        settings.EMAIL_HOST_USER
        if getattr(settings, 'EMAIL_HOST_USER', '')
        else 'noreply@campusconnect.com'
    )

    subject = f"New Placement Opportunity: {company_name}"
    body = (
        f"Hello,\n\n"
        f"A new placement opportunity has been posted for {company_name} ({post_title}).\n"
        f"Application deadline: {deadline_str}.\n\n"
        f"Log in to CampusConnect and apply as soon as possible!\n\n"
        f"Best regards,\n"
        f"CampusConnect Placements Team"
    )

    # send_mass_mail opens a single SMTP connection for all messages (efficient).
    messages = [
        (subject, body, from_email, [student.email])
        for student in students
    ]

    send_mass_mail(messages, fail_silently=False)
    logger.info(
        f'[placement_notification] Sent {len(messages)} emails for '
        f'{company_name!r} — task id {self.request.id}'
    )
