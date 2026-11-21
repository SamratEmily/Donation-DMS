from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import admin_required, volunteer_required
from .models import Volunteer
from .forms import VolunteerStatusForm


@admin_required
def volunteer_list(request):
    """
    Admin view to list all volunteers with filtering.
    """
    status_filter = request.GET.get('status', '')
    
    volunteers = Volunteer.objects.all().select_related('user', 'assigned_area')
    
    if status_filter:
        volunteers = volunteers.filter(status=status_filter)
    
    return render(request, 'volunteers/admin_volunteer_list.html', {
        'volunteers': volunteers,
        'status_filter': status_filter,
        'status_choices': Volunteer.STATUS_CHOICES
    })


@admin_required
def volunteer_detail(request, pk):
    """
    Admin view to see volunteer details and update status.
    """
    volunteer = get_object_or_404(Volunteer, pk=pk)
    
    if request.method == 'POST':
        form = VolunteerStatusForm(request.POST, instance=volunteer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Volunteer {volunteer.user.get_full_name()} updated successfully!')
            return redirect('volunteers:volunteer_list')
    else:
        form = VolunteerStatusForm(instance=volunteer)
    
    return render(request, 'volunteers/volunteer_detail.html', {
        'volunteer': volunteer,
        'form': form
    })


@admin_required
def accept_volunteer(request, pk):
    """
    Admin accepts a volunteer application.
    """
    volunteer = get_object_or_404(Volunteer, pk=pk)
    if volunteer.status == 'PENDING':
        volunteer.status = 'ACCEPTED'
        volunteer.save()
        messages.success(request, f'Volunteer {volunteer.user.get_full_name()} accepted successfully!')
    else:
        messages.warning(request, 'This volunteer application cannot be accepted at this stage.')
    
    return redirect('volunteers:volunteer_list')


@admin_required
def reject_volunteer(request, pk):
    """
    Admin rejects a volunteer application.
    """
    volunteer = get_object_or_404(Volunteer, pk=pk)
    if volunteer.status == 'PENDING':
        volunteer.status = 'REJECTED'
        volunteer.save()
        messages.success(request, f'Volunteer {volunteer.user.get_full_name()} rejected.')
    else:
        messages.warning(request, 'This volunteer application cannot be rejected at this stage.')
    
    return redirect('volunteers:volunteer_list')


@admin_required
def delete_volunteer(request, pk):
    """
    Admin deletes a volunteer.
    """
    volunteer = get_object_or_404(Volunteer, pk=pk)
    user = volunteer.user
    volunteer_name = user.get_full_name()
    
    # Delete user (cascade will delete volunteer)
    user.delete()
    messages.success(request, f'Volunteer {volunteer_name} deleted successfully!')
    
    return redirect('volunteers:volunteer_list')


@volunteer_required
def volunteer_profile(request):
    """
    Volunteer can view their own profile.
    """
    # Get or create volunteer profile
    volunteer, created = Volunteer.objects.get_or_create(user=request.user)
    
    return render(request, 'volunteers/volunteer_profile.html', {
        'volunteer': volunteer
    })
