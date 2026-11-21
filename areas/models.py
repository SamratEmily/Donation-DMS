from django.db import models


class DonationArea(models.Model):
    """
    Geographic areas where donations can be distributed.
    Admins create and manage these areas.
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Donation Area'
        verbose_name_plural = 'Donation Areas'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_volunteer_count(self):
        """Return number of volunteers assigned to this area."""
        return self.volunteers.filter(status='ACCEPTED').count()
    
    def get_donation_count(self):
        """Return number of donations in this area."""
        return self.donations.count()
