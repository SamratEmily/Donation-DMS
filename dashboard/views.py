from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from accounts.decorators import admin_required, donor_required, volunteer_required
from donations.models import Donation, DonationCollectionRequest
from volunteers.models import Volunteer
from donors.models import Donor
from areas.models import DonationArea


STATUS_COLORS = {
    'NEW': '#f5a524',
    'ACCEPTED': '#0ea5e9',
    'COLLECTED': '#6366f1',
    'DELIVERED': '#16a34a',
    'REJECTED': '#f43f5e',
}


def status_breakdown(queryset):
    """Return [{code, label, count, pct, color}] for each donation status."""
    counts = dict(queryset.order_by().values_list('status').annotate(n=Count('id')))
    total = sum(counts.values()) or 1
    return [
        {
            'code': code,
            'label': label,
            'count': counts.get(code, 0),
            'pct': round(counts.get(code, 0) * 100 / total, 1),
            'color': STATUS_COLORS[code],
        }
        for code, label in Donation.STATUS_CHOICES
    ]


@login_required
def index(request):
    """
    Main dashboard - routes users to their role-specific dashboard.
    """
    if request.user.is_admin():
        return admin_dashboard(request)
    elif request.user.is_donor():
        return donor_dashboard(request)
    elif request.user.is_volunteer():
        return volunteer_dashboard(request)
    else:
        return redirect('accounts:login')


@admin_required
def admin_dashboard(request):
    """
    Admin dashboard with statistics and management overview.
    """
    # Statistics
    total_donations = Donation.objects.count()
    new_donations = Donation.objects.filter(status='NEW').count()
    accepted_donations = Donation.objects.filter(status='ACCEPTED').count()
    collected_donations = Donation.objects.filter(status='COLLECTED').count()
    delivered_donations = Donation.objects.filter(status='DELIVERED').count()
    
    total_donors = Donor.objects.count()
    total_volunteers = Volunteer.objects.count()
    pending_volunteers = Volunteer.objects.filter(status='PENDING').count()
    accepted_volunteers = Volunteer.objects.filter(status='ACCEPTED').count()
    
    total_areas = DonationArea.objects.filter(is_active=True).count()
    
    # Recent donations
    recent_donations = Donation.objects.all().select_related('donor__user', 'area')[:10]
    
    # Pending volunteers
    pending_volunteer_list = Volunteer.objects.filter(status='PENDING').select_related('user')[:5]
    
    context = {
        'total_donations': total_donations,
        'new_donations': new_donations,
        'accepted_donations': accepted_donations,
        'collected_donations': collected_donations,
        'delivered_donations': delivered_donations,
        'total_donors': total_donors,
        'total_volunteers': total_volunteers,
        'pending_volunteers': pending_volunteers,
        'accepted_volunteers': accepted_volunteers,
        'total_areas': total_areas,
        'recent_donations': recent_donations,
        'pending_volunteer_list': pending_volunteer_list,
        'breakdown': status_breakdown(Donation.objects.all()),
        'areas': DonationArea.objects.filter(is_active=True).annotate(
            n_donations=Count('donations', distinct=True),
            n_volunteers=Count('volunteers', filter=Q(volunteers__status='ACCEPTED'), distinct=True),
        ).order_by('-n_donations')[:5],
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)


@donor_required
def donor_dashboard(request):
    """
    Donor dashboard with donation statistics and recent history.
    """
    # Check if donor profile exists
    try:
        donor = request.user.donor_profile
    except Donor.DoesNotExist:
        # Redirect to donor profile creation if it doesn't exist
        return redirect('donors:donor_profile')
    
    # Statistics
    total_donations = donor.donations.count()
    new_donations = donor.donations.filter(status='NEW').count()
    accepted_donations = donor.donations.filter(status='ACCEPTED').count()
    collected_donations = donor.donations.filter(status='COLLECTED').count()
    delivered_donations = donor.donations.filter(status='DELIVERED').count()
    rejected_donations = donor.donations.filter(status='REJECTED').count()
    
    # Recent donations
    recent_donations = donor.donations.all()[:5]
    
    context = {
        'donor': donor,
        'total_donations': total_donations,
        'new_donations': new_donations,
        'accepted_donations': accepted_donations,
        'collected_donations': collected_donations,
        'delivered_donations': delivered_donations,
        'rejected_donations': rejected_donations,
        'recent_donations': recent_donations,
        'breakdown': status_breakdown(donor.donations.all()),
    }
    
    return render(request, 'dashboard/donor_dashboard.html', context)


@volunteer_required
def volunteer_dashboard(request):
    """
    Volunteer dashboard with assigned donations and collection requests.
    """
    # Check if volunteer profile exists
    try:
        volunteer = request.user.volunteer_profile
    except Volunteer.DoesNotExist:
        # Redirect to volunteer profile creation if it doesn't exist
        return redirect('volunteers:volunteer_profile')
    
    # Check volunteer status
    if volunteer.status == 'PENDING':
        context = {
            'volunteer': volunteer,
            'status': 'pending'
        }
        return render(request, 'dashboard/volunteer_dashboard.html', context)
    
    elif volunteer.status == 'REJECTED':
        context = {
            'volunteer': volunteer,
            'status': 'rejected'
        }
        return render(request, 'dashboard/volunteer_dashboard.html', context)
    
    # Accepted volunteer
    assigned_donations_count = 0
    pending_collections = 0
    in_progress_collections = 0
    completed_collections = 0
    recent_donations = []
    recent_collections = DonationCollectionRequest.objects.filter(
        volunteer=volunteer
    ).select_related('donation__area').order_by('-updated_at')[:5]

    if volunteer.assigned_area:
        assigned_donations_count = Donation.objects.filter(
            area=volunteer.assigned_area,
            status='ACCEPTED'
        ).count()
        
        # Collection request statistics
        my_collections = DonationCollectionRequest.objects.filter(volunteer=volunteer)
        pending_collections = my_collections.filter(status='PENDING').count()
        in_progress_collections = my_collections.filter(status='IN_PROGRESS').count()
        completed_collections = my_collections.filter(status='COMPLETED').count()
        
        # Recent donations in assigned area
        recent_donations = Donation.objects.filter(
            area=volunteer.assigned_area,
            status='ACCEPTED'
        ).select_related('donor__user', 'area')[:5]
    
    context = {
        'volunteer': volunteer,
        'status': 'accepted',
        'assigned_donations_count': assigned_donations_count,
        'pending_collections': pending_collections,
        'in_progress_collections': in_progress_collections,
        'completed_collections': completed_collections,
        'recent_donations': recent_donations,
        'recent_collections': recent_collections,
    }
    
    return render(request, 'dashboard/volunteer_dashboard.html', context)
