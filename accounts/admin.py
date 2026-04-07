from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Skill, SemesterGPA


class SemesterGPAInline(admin.TabularInline):
    model = SemesterGPA
    extra = 1

@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'user_type', 'branch', 'is_verified', 'profile_completed')
    list_filter = ('user_type', 'branch', 'is_verified', 'profile_completed')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'current_company')
    list_editable = ('is_verified',)
    inlines = [SemesterGPAInline]

    fieldsets = UserAdmin.fieldsets + (
        ('CampusConnect Profile', {
            'fields': ('user_type', 'profile_pic', 'bio', 'branch', 'semester', 'cgpa',
                       'graduation_year', 'current_company', 'current_role',
                       'skills', 'resume', 'github_url', 'linkedin_url',
                       'portfolio_url', 'is_verified', 'profile_completed', 'college_email')
        }),
    )
    filter_horizontal = ('skills', 'groups', 'user_permissions')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SemesterGPA)
class SemesterGPAAdmin(admin.ModelAdmin):
    list_display = ('user', 'semester', 'gpa')
    list_filter = ('semester',)
    search_fields = ('user__username', 'user__email')
