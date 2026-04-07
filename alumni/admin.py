from django.contrib import admin
from .models import AlumniPost, MentorshipRequest, AlumniQuery

@admin.register(AlumniPost)
class AlumniPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_type', 'created_at')
    list_filter = ('post_type', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-created_at',)

@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_alumni', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('from_user__username', 'to_alumni__username')

@admin.register(AlumniQuery)
class AlumniQueryAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_alumni', 'is_answered', 'created_at')
    list_filter = ('is_answered', 'created_at')
    search_fields = ('from_user__username', 'to_alumni__username', 'question')
