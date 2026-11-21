from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/donor/', views.donor_signup, name='donor_signup'),
    path('signup/volunteer/', views.volunteer_signup, name='volunteer_signup'),
]

