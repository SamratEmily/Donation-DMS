from django.urls import path
from . import views

app_name = 'areas'

urlpatterns = [
    path('admin/list/', views.area_list, name='area_list'),
    path('admin/create/', views.area_create, name='area_create'),
    path('admin/edit/<int:pk>/', views.area_edit, name='area_edit'),
    path('admin/delete/<int:pk>/', views.area_delete, name='area_delete'),
]

