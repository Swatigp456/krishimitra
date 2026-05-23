from django.db import models
from core.models import Farmer

class Crop(models.Model):
    SEASON_CHOICES = [
        ('kharif', 'Kharif (June-October)'),
        ('rabi', 'Rabi (October-March)'),
        ('zaid', 'Zaid (March-June)'),
    ]
    
    name = models.CharField(max_length=50)
    name_hi = models.CharField(max_length=50, blank=True)
    name_pa = models.CharField(max_length=50, blank=True)
    scientific_name = models.CharField(max_length=100, blank=True)
    season = models.CharField(max_length=10, choices=SEASON_CHOICES)
    sowing_period = models.CharField(max_length=100)
    harvesting_period = models.CharField(max_length=100)
    image = models.ImageField(upload_to='crops/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class CropAdvisory(models.Model):
    GROWTH_STAGES = [
        ('sowing', 'Sowing'),
        ('germination', 'Germination'),
        ('vegetative', 'Vegetative Growth'),
        ('flowering', 'Flowering'),
        ('fruiting', 'Fruiting'),
        ('harvesting', 'Harvesting'),
    ]
    
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='advisories')
    growth_stage = models.CharField(max_length=20, choices=GROWTH_STAGES)
    weather_condition = models.CharField(max_length=100, default='normal')
    title = models.CharField(max_length=200)
    advice = models.TextField()
    advice_hi = models.TextField(blank=True)
    priority = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['priority', 'growth_stage']
    
    def __str__(self):
        return f"{self.crop.name} - {self.get_growth_stage_display()}"

class FarmerCrop(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='crops')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in acres")
    sowing_date = models.DateField()
    expected_harvest = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.farmer.username} - {self.crop.name} ({self.area} acres)"