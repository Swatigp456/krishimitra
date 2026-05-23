from django.contrib.auth.models import AbstractUser
from django.db import models

class Farmer(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    land_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preferred_language = models.CharField(max_length=10, default='en', choices=[
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('kn', 'Kannada'),
    ])
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} - {self.village}"

class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    
    def __str__(self):
        return self.name