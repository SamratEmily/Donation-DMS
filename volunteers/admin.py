from django.contrib import admin
from .models import Volunteer


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    """
    Admin interface for Volunteer model.
    """
    list_display = ('get_full_name', 'get_email', 'phone', 'status', 'assigned_area', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone')
    list_filter = ('status', 'assigned_area', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone',)
        }),
        ('Status & Assignment', {
            'fields': ('status', 'assigned_area')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
