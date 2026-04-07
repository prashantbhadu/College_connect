from django.urls import path
from . import views

app_name = 'alumni'

urlpatterns = [
    path('', views.alumni_directory, name='directory'),
    path('posts/', views.alumni_post_list, name='post_list'),
    path('posts/create/', views.alumni_post_create, name='post_create'),
    path('posts/<int:pk>/', views.alumni_post_detail, name='post_detail'),
    path('posts/<int:pk>/like/', views.like_post, name='like_post'),
    path('<int:alumni_pk>/request-mentorship/', views.mentorship_request, name='mentorship_request'),
    path('mentorship/', views.my_mentorship_requests, name='my_mentorship'),
    path('mentorship/<int:pk>/respond/', views.respond_mentorship, name='respond_mentorship'),
    path('<int:alumni_pk>/ask/', views.ask_query, name='ask_query'),
    path('queries/', views.my_queries, name='my_queries'),
    path('queries/<int:pk>/answer/', views.answer_query, name='answer_query'),
]
