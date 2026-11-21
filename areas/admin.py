from django.contrib import admin
from .models import DonationArea


@admin.register(DonationArea)
class DonationAreaAdmin(admin.ModelAdmin):
    """
    Admin interface for DonationArea model.
    """
    list_display = ('name', 'is_active', 'get_volunteer_count', 'get_donation_count', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
