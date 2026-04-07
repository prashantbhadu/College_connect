from django.db import models
from accounts.models import UserProfile


class ResumeAnalysis(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='analyses')
    resume_file = models.FileField(upload_to='resume_analyses/')
    target_role = models.CharField(max_length=200, blank=True)
    ats_score = models.IntegerField(default=0)
    analysis_result = models.JSONField(default=dict)
    suggestions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Analysis for {self.user.username} - Score: {self.ats_score}"
