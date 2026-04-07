from django.db import models
from accounts.models import UserProfile


class PlacementPost(models.Model):
    ROLE_TYPE_CHOICES = [
        ('fulltime', 'Full Time'),
        ('internship', 'Internship'),
        ('parttime', 'Part Time'),
    ]

    company_name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    role_type = models.CharField(max_length=20, choices=ROLE_TYPE_CHOICES, default='fulltime')
    ctc = models.CharField(max_length=100, blank=True, help_text='e.g. 12 LPA or 30K/month')
    eligibility_criteria = models.TextField(blank=True)
    deadline = models.DateField()
    application_link = models.URLField(blank=True)
    description = models.TextField()
    posted_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='placement_posts')
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company_name} - {self.role}"


class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('offered', 'Offered'),
    ]

    post = models.ForeignKey(PlacementPost, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('post', 'user')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.user.username} → {self.post.company_name}"


class CompanyThread(models.Model):
    post = models.ForeignKey(PlacementPost, on_delete=models.CASCADE, related_name='threads')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='thread_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Thread by {self.author.username} on {self.post.company_name}"
