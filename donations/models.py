from django.db import models
from django.conf import settings
from donors.models import Donor
from volunteers.models import Volunteer
from areas.models import DonationArea


class Donation(models.Model):
    """
    Donation model - tracks the complete lifecycle of a donation.
    Status flow: NEW -> ACCEPTED -> COLLECTED -> DELIVERED
    """
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('ACCEPTED', 'Accepted'),
        ('COLLECTED', 'Collected'),
        ('DELIVERED', 'Delivered'),
        ('REJECTED', 'Rejected'),
    )
    
    DONATION_TYPE_CHOICES = (
        ('FOOD', 'Food'),
        ('CLOTHES', 'Clothes'),
        ('MONEY', 'Money'),
        ('BOOKS', 'Books'),
        ('TOYS', 'Toys'),
        ('MEDICINE', 'Medicine'),
        ('OTHER', 'Other'),
    )
    
    donor = models.ForeignKey(
        Donor,
        on_delete=models.CASCADE,
        related_name='donations'
    )
    donation_type = models.CharField(
        max_length=20,
        choices=DONATION_TYPE_CHOICES
    )
    quantity = models.CharField(
        max_length=100,
        help_text='Quantity or amount (e.g., "5 kg", "$100", "10 items")'
    )
    description = models.TextField(blank=True)
    area = models.ForeignKey(
        DonationArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='donations'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='NEW'
    )
    admin_remark = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_donation_type_display()} - {self.donor.user.get_full_name()} - {self.get_status_display()}"
    
    def is_new(self):
        return self.status == 'NEW'
    
    def is_accepted(self):
        return self.status == 'ACCEPTED'
    
    def is_collected(self):
        return self.status == 'COLLECTED'
    
    def is_delivered(self):
        return self.status == 'DELIVERED'


class DonationCollectionRequest(models.Model):
    """
    Tracks volunteer collection requests for donations.
    Links volunteers to donations for collection and delivery.
    """
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )
    
    donation = models.OneToOneField(
        Donation,
        on_delete=models.CASCADE,
        related_name='collection_request'
    )
    volunteer = models.ForeignKey(
        Volunteer,
        on_delete=models.CASCADE,
        related_name='collection_requests'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    notes = models.TextField(blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Donation Collection Request'
        verbose_name_plural = 'Donation Collection Requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.donation} - {self.volunteer.user.get_full_name()} - {self.get_status_display()}"
