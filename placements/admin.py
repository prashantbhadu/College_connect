from django.contrib import admin
from .models import PlacementPost, Application, CompanyThread

class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    readonly_fields = ('user', 'applied_at')
    can_delete = False

@admin.register(PlacementPost)
class PlacementPostAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'role', 'role_type', 'ctc', 'min_cgpa', 'deadline', 'is_active', 'posted_by')
    list_filter = ('role_type', 'is_active', 'deadline')
    search_fields = ('company_name', 'role', 'description')
    ordering = ('-created_at',)
    inlines = [ApplicationInline]

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('user__username', 'post__company_name')

@admin.register(CompanyThread)
class CompanyThreadAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')

print("PLACEMENTS ADMIN LOADED")