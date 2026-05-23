from django.db import models
from crops.models import Crop
from core.models import Farmer

class Market(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return f"{self.name}, {self.city}"

class Price(models.Model):
    TREND_CHOICES = [
        ('up', '📈 Up'),
        ('down', '📉 Down'),
        ('stable', '➡️ Stable'),
    ]
    
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='prices')
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='prices')
    price_per_quintal = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    trend = models.CharField(max_length=10, choices=TREND_CHOICES, default='stable')
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.crop.name} @ {self.market.name}: ₹{self.price_per_quintal}"

class PriceAlert(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='price_alerts')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Alert: {self.crop.name} @ ₹{self.target_price} for {self.farmer.username}"