import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PlacementPost

logger = logging.getLogger(__name__)


@receiver(post_save, sender=PlacementPost)
def notify_students_new_placement(sender, instance, created, **kwargs):
    """
    Fires when a new PlacementPost is created.
    Enqueues a Celery task to send emails asynchronously.
    Includes exception handling so that if the Redis broker is temporarily down,
    the placement creation STILL succeeds without crashing the HTTP request.
    """
    if created and instance.is_active:
        from .tasks import send_placement_notification

        deadline_str = (
            instance.deadline.strftime('%B %d, %Y')
            if instance.deadline
            else 'not specified'
        )

        try:
            # .delay() pushes the task to Redis.
            send_placement_notification.delay(
                post_title=instance.role,
                company_name=instance.company_name,
                deadline_str=deadline_str,
            )
            logger.info(f"Queued notification email task for '{instance.company_name}' placement post.")
        except Exception as e:
            # Defensive programming: If Redis is offline or connection fails,
            # log the error but DO NOT crash the placement post creation!
            logger.error(
                f"Could not queue Celery email task for '{instance.company_name}'. "
                f"Error: {e}. Ensure Redis container is running."
            )
