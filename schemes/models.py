from django.db import models
from core.models import Farmer

class GovernmentScheme(models.Model):
    """Complete Government Schemes for Farmers"""
    
    CATEGORY_CHOICES = [
        ('income_support', 'Income Support'),
        ('insurance', 'Crop Insurance'),
        ('credit_loan', 'Credit & Loan'),
        ('infrastructure', 'Infrastructure'),
        ('mechanization', 'Farm Mechanization'),
        ('irrigation', 'Irrigation'),
        ('organic_farming', 'Organic Farming'),
        ('horticulture', 'Horticulture'),
        ('seed_planting', 'Seed & Planting'),
        ('marketing', 'Marketing'),
        ('digital_agri', 'Digital Agriculture'),
        ('pension', 'Pension & Welfare'),
    ]
    
    name = models.CharField(max_length=200)
    name_hi = models.CharField(max_length=200, blank=True)
    short_description = models.TextField()
    description = models.TextField()
    benefits = models.TextField()
    eligibility = models.TextField()
    application_process = models.TextField()
    documents_required = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='income_support')
    financial_assistance = models.CharField(max_length=200, blank=True)
    deadline = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)
    icon = models.CharField(max_length=10, default='📜')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class SchemeApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('document_required', 'More Documents Required'),
    ]
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='scheme_applications')
    scheme = models.ForeignKey(GovernmentScheme, on_delete=models.CASCADE, related_name='applications')
    applied_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    application_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.farmer.username} - {self.scheme.name}"