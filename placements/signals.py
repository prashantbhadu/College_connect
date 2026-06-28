from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PlacementPost
from .utils import send_placement_emails_async

@receiver(post_save, sender=PlacementPost)
def notify_students_new_placement(sender, instance, created, **kwargs):
    """
    Signal to trigger an email notification when a new placement is created.
    """
    if created and instance.is_active:
        send_placement_emails_async(
            post_title=instance.role,
            company_name=instance.company_name,
            deadline=instance.deadline
        )
