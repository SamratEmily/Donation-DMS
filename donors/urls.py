from django.urls import path
from . import views

app_name = 'donors'

urlpatterns = [
    # Admin URLs
    path('admin/list/', views.donor_list, name='donor_list'),
    path('admin/detail/<int:pk>/', views.donor_detail, name='donor_detail'),
    path('admin/delete/<int:pk>/', views.delete_donor, name='delete_donor'),
    
    # Donor URLs
    path('profile/', views.donor_profile, name='donor_profile'),
]

