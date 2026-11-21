from django.contrib import admin
from .models import Gallery


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """
    Admin interface for Gallery model.
    """
    list_display = (
        'id',
        'get_donation_info',
        'caption',
        'get_uploaded_by',
        'uploaded_at'
    )
    search_fields = (
        'donation__donor__user__email',
        'caption',
        'uploaded_by__email'
    )
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)
    
    def get_donation_info(self, obj):
        return f"Donation #{obj.donation.id} - {obj.donation.get_donation_type_display()}"
    get_donation_info.short_description = 'Donation'
    
    def get_uploaded_by(self, obj):
        if obj.uploaded_by:
            return obj.uploaded_by.get_full_name()
        return 'N/A'
    get_uploaded_by.short_description = 'Uploaded By'
