from django import forms
from .models import Donor


class DonorProfileForm(forms.ModelForm):
    """
    Form for updating donor profile information.
    """
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter your address'
        })
    )
    
    class Meta:
        model = Donor
        fields = ('phone', 'address')


