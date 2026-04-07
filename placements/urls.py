from django.urls import path
from . import views

app_name = 'placements'

urlpatterns = [
    path('', views.placement_list, name='list'),
    path('create/', views.placement_create, name='create'),
    path('<int:pk>/', views.placement_detail, name='detail'),
    path('<int:pk>/edit/', views.placement_update, name='edit'),
    path('<int:pk>/delete/', views.placement_delete, name='delete'),
    path('<int:pk>/apply/', views.apply_placement, name='apply'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('calendar/', views.placement_calendar, name='calendar'),
]
