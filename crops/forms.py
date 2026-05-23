from django import forms
from .models import FarmerCrop, Crop

class FarmerCropForm(forms.ModelForm):
    class Meta:
        model = FarmerCrop
        fields = ['crop', 'area', 'sowing_date', 'expected_harvest', 'notes']
        widgets = {
            'sowing_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_harvest': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }