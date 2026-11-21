from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import DonorSignupForm, VolunteerSignupForm, LoginForm
from donors.models import Donor
from volunteers.models import Volunteer
from donations.models import Donation
from areas.models import DonationArea


def login_view(request):
    """
    Handle user login for all roles.
    """
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('dashboard:index')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def donor_signup(request):
    """
    Handle donor registration.
    """
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = DonorSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create associated Donor profile
            Donor.objects.create(user=user)
            messages.success(request, 'Registration successful! Please login.')
            return redirect('accounts:login')
    else:
        form = DonorSignupForm()
    
    return render(request, 'accounts/donor_signup.html', {'form': form})


def volunteer_signup(request):
    """
    Handle volunteer registration.
    """
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = VolunteerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create associated Volunteer profile with PENDING status
            Volunteer.objects.create(user=user, status='PENDING')
            messages.success(request, 'Registration successful! Your application is pending approval.')
            return redirect('accounts:login')
    else:
        form = VolunteerSignupForm()
    
    return render(request, 'accounts/volunteer_signup.html', {'form': form})


@login_required
def logout_view(request):
    """
    Handle user logout.
    """
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


def home_view(request):
    """
    Landing page that shows login/signup options and recent donations.
    """
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    # Get statistics
    total_donations = Donation.objects.count()
    delivered_donations = Donation.objects.filter(status='DELIVERED').count()
    total_volunteers = Volunteer.objects.filter(status='ACCEPTED').count()
    total_areas = DonationArea.objects.filter(is_active=True).count()
    
    # Get recent delivered donations for display
    recent_donations = Donation.objects.filter(status='DELIVERED').order_by('-updated_at')[:6]
    
    context = {
        'total_donations': total_donations,
        'delivered_donations': delivered_donations,
        'total_volunteers': total_volunteers,
        'total_areas': total_areas,
        'recent_donations': recent_donations,
    }
    
    return render(request, 'accounts/home.html', context)

