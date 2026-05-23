from django.db import models
from core.models import Farmer
from crops.models import Crop

class Buyer(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ProductListing(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending Sale'),
        ('sold', 'Sold'),
        ('expired', 'Expired'),
    ]
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='listings')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="In quintals")
    price_per_quintal = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    quality = models.CharField(max_length=50, default='Standard', choices=[
        ('Premium', 'Premium Quality'),
        ('Standard', 'Standard Quality'),
        ('Fair', 'Fair Quality'),
    ])
    harvest_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.crop.name} - {self.quantity} qty by {self.farmer.username}"

class BuyerRequest(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='requests')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity_needed = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.buyer.name} needs {self.crop.name} ({self.quantity_needed} qty)"

class Interest(models.Model):
    """When a buyer shows interest in a farmer's listing"""
    listing = models.ForeignKey(ProductListing, on_delete=models.CASCADE, related_name='interests')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    offered_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity_requested = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('negotiating', 'Negotiating'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Interest from {self.buyer.name} on {self.listing.crop.name}"

class ChatMessage(models.Model):
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='messages')
    sender_type = models.CharField(max_length=10, choices=[('farmer', 'Farmer'), ('buyer', 'Buyer')])
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Message from {self.sender_type}"