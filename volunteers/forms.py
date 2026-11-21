from django import forms
from .models import Volunteer


class VolunteerProfileForm(forms.ModelForm):
    """
    Form for updating volunteer profile information.
    """
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )
    
    class Meta:
        model = Volunteer
        fields = ('phone',)


class VolunteerStatusForm(forms.ModelForm):
    """
    Form for admin to update volunteer status and assignment.
    """
    class Meta:
        model = Volunteer
        fields = ('status', 'assigned_area')
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_area': forms.Select(attrs={'class': 'form-select'}),
        }


