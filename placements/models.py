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


class PlacementRecord(models.Model):
    PLACEMENT_STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('internship', 'Internship'),
        ('ppo', 'PPO'),
    ]

    student = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='placement_records',
        limit_choices_to={'user_type': 'student'},
    )
    placement_post = models.ForeignKey(
        PlacementPost,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='placement_records',
    )
    company_name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    role_type = models.CharField(
        max_length=20,
        choices=PlacementPost.ROLE_TYPE_CHOICES,
        default='fulltime',
    )
    placement_status = models.CharField(
        max_length=20,
        choices=PLACEMENT_STATUS_CHOICES,
        default='placed',
    )
    placement_year = models.PositiveIntegerField()
    branch = models.CharField(max_length=10, choices=UserProfile.BRANCH_CHOICES, blank=True)
    package_lpa = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    package_display = models.CharField(max_length=100, blank=True, help_text='e.g. 12 LPA or 35K/month')
    location = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recorded_placements',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-placement_year', 'company_name', 'student__username']

    def save(self, *args, **kwargs):
        if not self.branch and self.student.branch:
            self.branch = self.student.branch
        if not self.placement_year and self.student.graduation_year:
            self.placement_year = self.student.graduation_year
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.company_name} ({self.placement_year})"
