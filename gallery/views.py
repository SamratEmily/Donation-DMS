from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required, volunteer_required
from .models import Gallery
from .forms import GalleryImageForm
from donations.models import Donation


@login_required
def upload_image(request, donation_id):
    """
    Upload delivery image for a donation.
    Both admin and volunteers can upload images.
    """
    donation = get_object_or_404(Donation, pk=donation_id)
    
    # Check permissions
    if not (request.user.is_admin() or 
            (request.user.is_volunteer() and 
             request.user.volunteer_profile.assigned_area == donation.area)):
        messages.error(request, 'You do not have permission to upload images for this donation.')
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            gallery_image = form.save(commit=False)
            gallery_image.donation = donation
            gallery_image.uploaded_by = request.user
            gallery_image.save()
            
            # Update donation status to DELIVERED if it's COLLECTED
            if donation.status == 'COLLECTED':
                donation.status = 'DELIVERED'
                donation.save()
            
            messages.success(request, 'Image uploaded successfully!')
            return redirect('gallery:donation_gallery', donation_id=donation.id)
    else:
        form = GalleryImageForm()
    
    return render(request, 'gallery/upload_image.html', {
        'form': form,
        'donation': donation
    })


@login_required
def donation_gallery(request, donation_id):
    """
    View all images for a specific donation.
    """
    donation = get_object_or_404(Donation, pk=donation_id)
    images = Gallery.objects.filter(donation=donation)
    
    return render(request, 'gallery/donation_gallery.html', {
        'donation': donation,
        'images': images
    })


@admin_required
def admin_gallery_list(request):
    """
    Admin view of all uploaded images.
    """
    images = Gallery.objects.all().select_related('donation', 'uploaded_by')
    
    return render(request, 'gallery/admin_gallery_list.html', {
        'images': images
    })


@admin_required
def delete_image(request, pk):
    """
    Admin can delete images.
    """
    image = get_object_or_404(Gallery, pk=pk)
    donation_id = image.donation.id
    image.delete()
    messages.success(request, 'Image deleted successfully!')
    return redirect('gallery:donation_gallery', donation_id=donation_id)
