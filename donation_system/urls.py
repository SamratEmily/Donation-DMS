"""
URL configuration for donation_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # App URLs
    path('', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('donations/', include('donations.urls')),
    path('volunteers/', include('volunteers.urls')),
    path('donors/', include('donors.urls')),
    path('areas/', include('areas.urls')),
    path('gallery/', include('gallery.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
