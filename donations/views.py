from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import donor_required, admin_required, volunteer_required
from .models import Donation, DonationCollectionRequest
from .forms import DonationForm, DonationUpdateForm, DonationCollectionForm
from django.utils import timezone


@donor_required
def create_donation(request):
    """
    Allow donors to create new donation requests.
    """
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user.donor_profile
            donation.save()
            messages.success(request, 'Donation request submitted successfully!')
            return redirect('donations:donor_donation_list')
    else:
        form = DonationForm()
    
    return render(request, 'donations/donation_form.html', {'form': form})


@donor_required
def donor_donation_list(request):
    """
    Show donation history for the logged-in donor.
    """
    donations = Donation.objects.filter(donor=request.user.donor_profile)
    return render(request, 'donations/donor_donation_list.html', {
        'donations': donations
    })


@donor_required
def donation_detail(request, pk):
    """
    Show detailed information about a specific donation.
    """
    donation = get_object_or_404(Donation, pk=pk, donor=request.user.donor_profile)
    return render(request, 'donations/donation_detail.html', {
        'donation': donation
    })


@admin_required
def admin_donation_list(request):
    """
    Show all donations for admin management.
    """
    status_filter = request.GET.get('status', '')
    
    donations = Donation.objects.all().select_related('donor__user', 'area')
    
    if status_filter:
        donations = donations.filter(status=status_filter)
    
    return render(request, 'donations/admin_donation_list.html', {
        'donations': donations,
        'status_filter': status_filter,
        'status_choices': Donation.STATUS_CHOICES
    })


@admin_required
def admin_donation_detail(request, pk):
    """
    Show donation details and allow admin to update status.
    """
    donation = get_object_or_404(Donation, pk=pk)
    
    if request.method == 'POST':
        form = DonationUpdateForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation updated successfully!')
            return redirect('donations:admin_donation_detail', pk=pk)
    else:
        form = DonationUpdateForm(instance=donation)
    
    return render(request, 'donations/admin_donation_detail.html', {
        'donation': donation,
        'form': form
    })


@admin_required
def accept_donation(request, pk):
    """
    Admin accepts a donation request.
    """
    donation = get_object_or_404(Donation, pk=pk)
    if donation.status == 'NEW':
        donation.status = 'ACCEPTED'
        donation.save()
        messages.success(request, f'Donation #{donation.id} accepted successfully!')
    else:
        messages.warning(request, 'This donation cannot be accepted at this stage.')
    
    return redirect('donations:admin_donation_list')


@admin_required
def reject_donation(request, pk):
    """
    Admin rejects a donation request.
    """
    donation = get_object_or_404(Donation, pk=pk)
    if donation.status == 'NEW':
        donation.status = 'REJECTED'
        if request.method == 'POST':
            donation.admin_remark = request.POST.get('remark', '')
        donation.save()
        messages.success(request, f'Donation #{donation.id} rejected.')
    else:
        messages.warning(request, 'This donation cannot be rejected at this stage.')
    
    return redirect('donations:admin_donation_list')


@volunteer_required
def volunteer_donation_list(request):
    """
    Show donations assigned to the volunteer's area.
    """
    volunteer = request.user.volunteer_profile
    
    # Check if volunteer is accepted and has an assigned area
    if volunteer.status != 'ACCEPTED':
        messages.warning(request, 'Your volunteer application is still pending approval.')
        return redirect('dashboard:index')
    
    if not volunteer.assigned_area:
        messages.info(request, 'You have not been assigned to any area yet.')
        return redirect('dashboard:index')
    
    # Get donations in the volunteer's assigned area with ACCEPTED status
    donations = Donation.objects.filter(
        area=volunteer.assigned_area,
        status='ACCEPTED'
    ).select_related('donor__user', 'area')
    
    return render(request, 'donations/volunteer_donation_list.html', {
        'donations': donations,
        'volunteer': volunteer
    })


@volunteer_required
def volunteer_donation_detail(request, pk):
    """
    Show donation details for volunteer and allow collection status updates.
    """
    volunteer = request.user.volunteer_profile
    donation = get_object_or_404(Donation, pk=pk, area=volunteer.assigned_area)
    
    # Get or create collection request
    collection_request, created = DonationCollectionRequest.objects.get_or_create(
        donation=donation,
        defaults={'volunteer': volunteer}
    )
    
    if request.method == 'POST':
        form = DonationCollectionForm(request.POST, instance=collection_request)
        if form.is_valid():
            collection = form.save(commit=False)
            if collection.status == 'COMPLETED':
                collection.collected_at = timezone.now()
                donation.status = 'COLLECTED'
                donation.save()
            collection.save()
            messages.success(request, 'Collection status updated successfully!')
            return redirect('donations:volunteer_donation_detail', pk=pk)
    else:
        form = DonationCollectionForm(instance=collection_request)
    
    return render(request, 'donations/volunteer_donation_detail.html', {
        'donation': donation,
        'collection_request': collection_request,
        'form': form
    })
