from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    # Donor URLs
    path('create/', views.create_donation, name='create_donation'),
    path('my-donations/', views.donor_donation_list, name='donor_donation_list'),
    path('detail/<int:pk>/', views.donation_detail, name='donation_detail'),
    
    # Admin URLs
    path('admin/list/', views.admin_donation_list, name='admin_donation_list'),
    path('admin/detail/<int:pk>/', views.admin_donation_detail, name='admin_donation_detail'),
    path('admin/accept/<int:pk>/', views.accept_donation, name='accept_donation'),
    path('admin/reject/<int:pk>/', views.reject_donation, name='reject_donation'),
    
    # Volunteer URLs
    path('volunteer/list/', views.volunteer_donation_list, name='volunteer_donation_list'),
    path('volunteer/detail/<int:pk>/', views.volunteer_donation_detail, name='volunteer_donation_detail'),
]

