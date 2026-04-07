from django.contrib import admin
from .models import ResumeAnalysis

@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_role', 'ats_score', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'target_role')
    ordering = ('-created_at',)
