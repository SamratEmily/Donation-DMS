from django.contrib import admin
from .models import Donation, DonationCollectionRequest


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    """
    Admin interface for Donation model.
    """
    list_display = (
        'id',
        'get_donor_name',
        'donation_type',
        'quantity',
        'area',
        'status',
        'created_at'
    )
    search_fields = (
        'donor__user__email',
        'donor__user__first_name',
        'donor__user__last_name',
        'donation_type',
        'description'
    )
    list_filter = ('status', 'donation_type', 'area', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor',)
        }),
        ('Donation Details', {
            'fields': ('donation_type', 'quantity', 'description', 'area')
        }),
        ('Status & Remarks', {
            'fields': ('status', 'admin_remark')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_donor_name(self, obj):
        return obj.donor.user.get_full_name()
    get_donor_name.short_description = 'Donor'


@admin.register(DonationCollectionRequest)
class DonationCollectionRequestAdmin(admin.ModelAdmin):
    """
    Admin interface for DonationCollectionRequest model.
    """
    list_display = (
        'id',
        'get_donation_info',
        'get_volunteer_name',
        'status',
        'collected_at',
        'created_at'
    )
    search_fields = (
        'donation__donor__user__email',
        'volunteer__user__email',
        'volunteer__user__first_name',
        'volunteer__user__last_name'
    )
    list_filter = ('status', 'created_at', 'collected_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_donation_info(self, obj):
        return f"{obj.donation.get_donation_type_display()} - {obj.donation.quantity}"
    get_donation_info.short_description = 'Donation'
    
    def get_volunteer_name(self, obj):
        return obj.volunteer.user.get_full_name()
    get_volunteer_name.short_description = 'Volunteer'
