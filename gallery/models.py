from django.db import models
from donations.models import Donation


class Gallery(models.Model):
    """
    Gallery model to store images of delivered donations.
    Both admins and volunteers can upload delivery images.
    """
    donation = models.ForeignKey(
        Donation,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='gallery/%Y/%m/%d/',
        help_text='Upload delivery image'
    )
    caption = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_images'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Image for Donation #{self.donation.id} - {self.uploaded_at.strftime('%Y-%m-%d')}"
