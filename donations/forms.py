from django import forms
from .models import Donation, DonationCollectionRequest


class DonationForm(forms.ModelForm):
    """
    Form for donors to create donation requests.
    """
    donation_type = forms.ChoiceField(
        choices=Donation.DONATION_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    quantity = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., "5 kg", "$100", "10 items"'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Additional details about the donation'
        })
    )
    
    class Meta:
        model = Donation
        fields = ('donation_type', 'quantity', 'description')


class DonationUpdateForm(forms.ModelForm):
    """
    Form for admin to update donation status and details.
    """
    area = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    status = forms.ChoiceField(
        choices=Donation.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    admin_remark = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Add remarks about this donation'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from areas.models import DonationArea
        self.fields['area'].queryset = DonationArea.objects.filter(is_active=True)
    
    class Meta:
        model = Donation
        fields = ('area', 'status', 'admin_remark')


class DonationCollectionForm(forms.ModelForm):
    """
    Form for volunteers to update collection status.
    """
    status = forms.ChoiceField(
        choices=DonationCollectionRequest.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Add notes about the collection'
        })
    )
    
    class Meta:
        model = DonationCollectionRequest
        fields = ('status', 'notes')


