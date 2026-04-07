from django.db import models
from accounts.models import UserProfile


class AlumniPost(models.Model):
    POST_TYPE_CHOICES = [
        ('insight', 'Industry Insight'),
        ('success', 'Success Story'),
        ('guidance', 'Career Guidance'),
        ('announcement', 'Announcement'),
    ]

    title = models.CharField(max_length=300)
    content = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='alumni_posts')
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='insight')
    tags = models.CharField(max_length=500, blank=True, help_text='Comma-separated tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(UserProfile, blank=True, related_name='liked_posts')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def get_tags_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]


class MentorshipRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='mentorship_requests_sent')
    to_alumni = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='mentorship_requests_received')
    message = models.TextField(max_length=1000)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('from_user', 'to_alumni')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user.username} → {self.to_alumni.username} [{self.status}]"


class AlumniQuery(models.Model):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='queries_asked')
    to_alumni = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='queries_received')
    question = models.TextField(max_length=2000)
    answer = models.TextField(blank=True)
    is_answered = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True, help_text='Show as public Q&A for others to see')
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Q from {self.from_user.username} to {self.to_alumni.username}"
