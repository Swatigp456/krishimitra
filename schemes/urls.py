from django.urls import path
from . import views

urlpatterns = [
    path('', views.schemes_list, name='schemes_list'),
    path('<int:scheme_id>/', views.scheme_detail, name='scheme_detail'),
    path('my-applications/', views.my_applications, name='my_applications'),
]