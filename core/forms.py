from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Farmer

class FarmerRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=True)
    village = forms.CharField(max_length=100, required=True, help_text="Your village name for accurate weather")
    district = forms.CharField(max_length=100, required=True, help_text="Your district")
    state = forms.CharField(max_length=100, required=True)
    land_size = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    
    class Meta:
        model = Farmer
        fields = ['username', 'first_name', 'last_name', 'phone', 'village', 'district', 'state', 'land_size', 'password1', 'password2']
        help_texts = {
            'village': 'Enter your village name for accurate local weather forecasts',
        }

class FarmerLoginForm(AuthenticationForm):
    class Meta:
        model = Farmer
        fields = ['username', 'password']