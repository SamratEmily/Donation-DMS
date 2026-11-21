from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import admin_required, donor_required
from .models import Donor
from .forms import DonorProfileForm


@admin_required
def donor_list(request):
    """
    Admin view to list all donors.
    """
    donors = Donor.objects.all().select_related('user')
    
    return render(request, 'donors/admin_donor_list.html', {
        'donors': donors
    })


@admin_required
def donor_detail(request, pk):
    """
    Admin view to see donor details and donation history.
    """
    donor = get_object_or_404(Donor, pk=pk)
    donations = donor.donations.all()
    
    return render(request, 'donors/donor_detail.html', {
        'donor': donor,
        'donations': donations
    })


@admin_required
def delete_donor(request, pk):
    """
    Admin deletes a donor.
    """
    donor = get_object_or_404(Donor, pk=pk)
    user = donor.user
    donor_name = user.get_full_name()
    
    # Delete user (cascade will delete donor)
    user.delete()
    messages.success(request, f'Donor {donor_name} deleted successfully!')
    
    return redirect('donors:donor_list')


@donor_required
def donor_profile(request):
    """
    Donor can view and update their own profile.
    """
    # Get or create donor profile
    donor, created = Donor.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = DonorProfileForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('donors:donor_profile')
    else:
        form = DonorProfileForm(instance=donor)
    
    return render(request, 'donors/donor_profile.html', {
        'donor': donor,
        'form': form
    })
