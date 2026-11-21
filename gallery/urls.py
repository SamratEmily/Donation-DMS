from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('upload/<int:donation_id>/', views.upload_image, name='upload_image'),
    path('donation/<int:donation_id>/', views.donation_gallery, name='donation_gallery'),
    path('admin/list/', views.admin_gallery_list, name='admin_gallery_list'),
    path('admin/delete/<int:pk>/', views.delete_image, name='delete_image'),
]


