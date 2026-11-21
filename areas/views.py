from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import admin_required
from .models import DonationArea
from .forms import DonationAreaForm


@admin_required
def area_list(request):
    """
    Admin view to list all donation areas.
    """
    areas = DonationArea.objects.all()
    
    return render(request, 'areas/area_list.html', {
        'areas': areas
    })


@admin_required
def area_create(request):
    """
    Admin creates a new donation area.
    """
    if request.method == 'POST':
        form = DonationAreaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation area created successfully!')
            return redirect('areas:area_list')
    else:
        form = DonationAreaForm()
    
    return render(request, 'areas/area_form.html', {
        'form': form,
        'action': 'Create'
    })


@admin_required
def area_edit(request, pk):
    """
    Admin edits an existing donation area.
    """
    area = get_object_or_404(DonationArea, pk=pk)
    
    if request.method == 'POST':
        form = DonationAreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation area updated successfully!')
            return redirect('areas:area_list')
    else:
        form = DonationAreaForm(instance=area)
    
    return render(request, 'areas/area_form.html', {
        'form': form,
        'action': 'Edit',
        'area': area
    })


@admin_required
def area_delete(request, pk):
    """
    Admin deletes a donation area.
    """
    area = get_object_or_404(DonationArea, pk=pk)
    area_name = area.name
    area.delete()
    messages.success(request, f'Donation area "{area_name}" deleted successfully!')
    
    return redirect('areas:area_list')
