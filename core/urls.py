from django.urls import path
from . import views
from . import ai_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('get-weather-api/', views.get_weather_api, name='get_weather_api'),
    path('set-language/', views.set_language, name='set_language'),
    path('switch-language/', views.switch_language, name='switch_language'),
    path('offline/', views.offline_page, name='offline'),
    
    # Smart Farming Tools
    path('disease-detection/', views.disease_detection, name='disease_detection'),
    path('fertilizer-calculator/', views.fertilizer_calculator, name='fertilizer_calculator'),
    path('harvest-predictor/', views.harvest_predictor, name='harvest_predictor'),
    path('nearby-services/', views.nearby_services, name='nearby_services'),
    
    # AI Routes
    path('ai-dashboard/', ai_views.ai_dashboard, name='ai_dashboard'),
    path('ai-chat/', ai_views.ai_chat, name='ai_chat'),
    path('ai-disease-prediction/', ai_views.ai_disease_prediction, name='ai_disease_prediction'),
    path('ai-yield-predictor/', ai_views.ai_yield_predictor, name='ai_yield_predictor'),
    path('ai-fertilizer-advisor/', ai_views.ai_fertilizer_advisor, name='ai_fertilizer_advisor'),
    path('ai-pest-predictor/', ai_views.ai_pest_predictor, name='ai_pest_predictor'),
    path('ai-farm-analysis/', ai_views.ai_farm_analysis, name='ai_farm_analysis'),
    # Add these to urlpatterns
    path('multimodal-analysis/', views.multimodal_analysis, name='multimodal_analysis'),
    path('voice-assistant/', views.get_voice_assistant, name='voice_assistant'),
    # core/urls.py - Add this if not exists
    path('ai-chat/', ai_views.ai_chat, name='ai_chat'),
]