from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('placements/', include('placements.urls')),
    path('alumni/', include('alumni.urls')),
    path('resume/', include('resume_analyzer.urls')),

    # REST API
    path('api/', include('accounts.api_urls')),
    path('api/', include('placements.api_urls')),
    path('api/', include('alumni.api_urls')),
    path('api/', include('resume_analyzer.api_urls')),
    path('api/', include('dashboard.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
