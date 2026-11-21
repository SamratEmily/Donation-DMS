from django.db import models
from django.conf import settings
from areas.models import DonationArea


class Volunteer(models.Model):
    """
    Volunteer model - OneToOne relationship with User.
    Volunteers must be approved by admin before they can access the system.
    """
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    )
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='volunteer_profile'
    )
    phone = models.CharField(max_length=15, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    assigned_area = models.ForeignKey(
        DonationArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='volunteers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Volunteer'
        verbose_name_plural = 'Volunteers'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_status_display()}"
    
    def is_accepted(self):
        """Check if volunteer is accepted."""
        return self.status == 'ACCEPTED'
    
    def get_assigned_donations_count(self):
        """Return count of assigned donations."""
        if self.assigned_area:
            return self.assigned_area.donations.filter(status='ACCEPTED').count()
        return 0
