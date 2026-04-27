from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.landing_page, name='home'),
    path('dashboard/', views.feed, name='feed'),
    path('search/', views.search, name='search'),
]
