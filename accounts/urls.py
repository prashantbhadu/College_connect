from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/student/', views.register_student, name='register_student'),
    path('register/alumni/', views.register_alumni, name='register_alumni'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='my_profile'),
    path('profile/<int:pk>/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
