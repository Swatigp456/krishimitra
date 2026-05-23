from django.db import models
from core.models import Farmer

class Inventory(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilograms'),
        ('g', 'Grams'),
        ('l', 'Liters'),
        ('ml', 'Milliliters'),
        ('pieces', 'Pieces'),
        ('bags', 'Bags'),
    ]
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='inventory')
    item_name = models.CharField(max_length=100)
    item_name_hi = models.CharField(max_length=100, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.item_name} - {self.quantity} {self.unit}"

class FarmTask(models.Model):
    PRIORITY_CHOICES = [
        ('high', '🔴 High'),
        ('medium', '🟡 Medium'),
        ('low', '🟢 Low'),
    ]
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['due_date', '-priority']
    
    def __str__(self):
        return self.title

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('seeds', '🌱 Seeds'),
        ('fertilizer', '🧪 Fertilizer'),
        ('pesticide', '🐛 Pesticide'),
        ('labor', '👨‍🌾 Labor'),
        ('irrigation', '💧 Irrigation'),
        ('equipment', '🔧 Equipment'),
        ('transport', '🚛 Transport'),
        ('other', '📦 Other'),
    ]
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_category_display()} - ₹{self.amount}"