from django.urls import path
from . import views

urlpatterns = [
    path('', views.farm_manager, name='farm_manager'),
    path('add-inventory/', views.add_inventory, name='add_inventory'),
    path('add-task/', views.add_task, name='add_task'),
    path('complete-task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('add-expense/', views.add_expense, name='add_expense'),
]