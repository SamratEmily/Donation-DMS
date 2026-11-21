from django import forms
from .models import Gallery


class GalleryImageForm(forms.ModelForm):
    """
    Form for uploading delivery images.
    """
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )
    caption = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Add a caption (optional)'
        })
    )
    
    class Meta:
        model = Gallery
        fields = ('image', 'caption')


