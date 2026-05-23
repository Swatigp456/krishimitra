from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import models
from .models import Inventory, FarmTask, Expense
from .forms import InventoryForm, TaskForm, ExpenseForm

@login_required
def farm_manager(request):
    inventory_items = Inventory.objects.filter(farmer=request.user)
    tasks = FarmTask.objects.filter(farmer=request.user)
    expenses = Expense.objects.filter(farmer=request.user)
    
    total_expenses = expenses.aggregate(total=models.Sum('amount'))['total'] or 0
    pending_tasks = tasks.filter(is_completed=False).count()
    completed_tasks = tasks.filter(is_completed=True).count()
    
    # Expense by category
    expense_by_category = {}
    for expense in expenses:
        cat = expense.get_category_display()
        expense_by_category[cat] = expense_by_category.get(cat, 0) + float(expense.amount)
    
    context = {
        'inventory_items': inventory_items,
        'tasks': tasks,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'expense_by_category': expense_by_category,
    }
    return render(request, 'farmmanager/dashboard.html', context)

@login_required
def add_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.farmer = request.user
            item.save()
    return redirect('farm_manager')

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.farmer = request.user
            task.save()
    return redirect('farm_manager')

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(FarmTask, id=task_id, farmer=request.user)
    task.is_completed = True
    task.save()
    return redirect('farm_manager')

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.farmer = request.user
            expense.save()
    return redirect('farm_manager')