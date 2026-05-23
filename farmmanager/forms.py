from django import forms
from .models import Inventory, FarmTask, Expense

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['item_name', 'quantity', 'unit', 'price', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = FarmTask
        fields = ['title', 'description', 'due_date', 'priority']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'e.g., Bought 2 bags of DAP'}),
        }