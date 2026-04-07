from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class UserProfile(AbstractUser):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('alumni', 'Alumni'),
        ('admin', 'Admin'),
    ]

    BRANCH_CHOICES = [
        ('CSE', 'Computer Science & Engineering'),
        ('ECE', 'Electronics & Communication Engineering'),
        ('EEE', 'Electrical & Electronics Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('IT', 'Information Technology'),
        ('CHE', 'Chemical Engineering'),
        ('BT', 'Biotechnology'),
        ('OTHER', 'Other'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(blank=True, max_length=500)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES, blank=True)
    semester = models.IntegerField(null=True, blank=True)  # for students
    graduation_year = models.IntegerField(null=True, blank=True)  # for alumni
    current_company = models.CharField(max_length=200, blank=True)  # for alumni
    current_role = models.CharField(max_length=200, blank=True)  # for alumni
    skills = models.ManyToManyField(Skill, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    profile_completed = models.BooleanField(default=False)
    college_email = models.EmailField(blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.user_type})"

    @property
    def is_student(self):
        return self.user_type == 'student'

    @property
    def is_alumni(self):
        return self.user_type == 'alumni'

    def get_profile_pic_url(self):
        if self.profile_pic:
            return self.profile_pic.url
        return '/static/images/default_avatar.png'


class SemesterGPA(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='semester_gpas')
    semester = models.IntegerField()
    gpa = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        unique_together = ('user', 'semester')
        ordering = ['semester']

    def __str__(self):
        return f"{self.user.username} - Sem {self.semester}: {self.gpa}"

    def update_user_cgpa(self):
        aggr = self.user.semester_gpas.aggregate(avg_gpa=Avg('gpa'))
        self.user.cgpa = aggr['avg_gpa']
        self.user.save(update_fields=['cgpa'])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_user_cgpa()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_user_cgpa()
