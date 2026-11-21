from django.db import models
from django.conf import settings


class Donor(models.Model):
    """
    Donor profile model - OneToOne relationship with User.
    Contains additional information about donors.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='donor_profile'
    )
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Donor'
        verbose_name_plural = 'Donors'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.email}"
    
    def get_total_donations(self):
        """Return total number of donations made by this donor."""
        return self.donations.count()
    
    def get_accepted_donations(self):
        """Return number of accepted donations."""
        return self.donations.filter(status='ACCEPTED').count()
