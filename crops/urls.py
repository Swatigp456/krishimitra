from django.urls import path
from . import views

urlpatterns = [
    path('advisory/', views.crop_advisory, name='crop_advisory'),
    path('my-crops/', views.my_crops, name='my_crops'),
    path('api/advisory/', views.get_advisory_api, name='api_advisory'),
]