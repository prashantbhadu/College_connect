from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
<<<<<<< HEAD
    path('', views.landing_page, name='home'),
=======
    path('', views.feed, name='home'),
>>>>>>> 95a4aa9 (Till the alumni, student and admin)
    path('dashboard/', views.feed, name='feed'),
    path('search/', views.search, name='search'),
]
