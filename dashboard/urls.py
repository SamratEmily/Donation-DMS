from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('donor/', views.donor_dashboard, name='donor_dashboard'),
    path('volunteer/', views.volunteer_dashboard, name='volunteer_dashboard'),
]


