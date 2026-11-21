from django.urls import path
from . import views

app_name = 'volunteers'

urlpatterns = [
    # Admin URLs
    path('admin/list/', views.volunteer_list, name='volunteer_list'),
    path('admin/detail/<int:pk>/', views.volunteer_detail, name='volunteer_detail'),
    path('admin/accept/<int:pk>/', views.accept_volunteer, name='accept_volunteer'),
    path('admin/reject/<int:pk>/', views.reject_volunteer, name='reject_volunteer'),
    path('admin/delete/<int:pk>/', views.delete_volunteer, name='delete_volunteer'),
    
    # Volunteer URLs
    path('profile/', views.volunteer_profile, name='volunteer_profile'),
]

