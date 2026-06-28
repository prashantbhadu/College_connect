import threading
from django.core.mail import send_mass_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_placement_emails_async(post_title, company_name, deadline):
    """
    Background task to send emails to all students about a new placement.
    """
    from accounts.models import UserProfile
    
    def send_emails():
        try:
            students = UserProfile.objects.filter(user_type='student', email__isnull=False).exclude(email='')
            if not students.exists():
                return
            
            subject = f"New Placement Opportunity: {company_name}"
            message = (
                f"Hello,\n\n"
                f"A new placement opportunity has arrived for {company_name} ({post_title}).\n"
                f"The application deadline is {deadline.strftime('%B %d, %Y') if deadline else 'not specified'}.\n\n"
                f"Apply as soon as possible to avoid missing the opportunity.\n\n"
                f"Best regards,\n"
                f"CampusConnect Placements Team"
            )
            from_email = settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER else 'noreply@campusconnect.com'
            
            # Prepare messages format for send_mass_mail: tuple of (subject, message, from_email, recipient_list)
            messages = [(subject, message, from_email, [student.email]) for student in students]
            
            # send_mass_mail opens a single connection to the SMTP server to send all messages
            send_mass_mail(messages, fail_silently=False)
            logger.info(f"Successfully sent {len(messages)} placement notification emails for {company_name}.")
            
        except Exception as e:
            logger.error(f"Failed to send placement notification emails: {str(e)}")

    # Start the thread
    thread = threading.Thread(target=send_emails)
    thread.daemon = True
    thread.start()
