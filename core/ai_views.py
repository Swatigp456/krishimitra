# core/ai_views.py - Complete Working Views
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .ai_services import ai_services
from .weather_utils import weather_service
import json

@login_required
def ai_dashboard(request):
    """AI Dashboard main view"""
    return render(request, 'core/ai_dashboard.html')

# ============ AI CHAT ============
@login_required
def ai_chat(request):
    """AI Chatbot endpoint"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '')
            # For chat, we'll use a simple response
            response = f"🌾 Thanks for asking: '{query}'\n\nPlease use the AI Prediction tools for:\n• Disease Prediction\n• Yield Prediction\n• Fertilizer Advice\n• Pest Prediction\n• Farm Analysis"
            return JsonResponse({'success': True, 'response': response})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# ============ DISEASE PREDICTION ============
@login_required
def ai_disease_prediction(request):
    """AI Disease Prediction API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            crop_name = data.get('crop', 'rice')
            growth_stage = data.get('stage', 'vegetative')
            
            location = request.user.village or request.user.district or "Delhi"
            weather = weather_service.get_current_weather(location)
            
            result = ai_services.predict_disease_risk(crop_name, weather, growth_stage)
            return JsonResponse({'success': True, 'prediction': result})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# ============ YIELD PREDICTION ============
@login_required
def ai_yield_predictor(request):
    """AI Yield Prediction API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            crop_name = data.get('crop', 'rice')
            area = data.get('area', 1)
            soil_quality = data.get('soil', 'medium')
            
            location = request.user.village or request.user.district or "Delhi"
            weather = weather_service.get_current_weather(location)
            
            result = ai_services.predict_yield(crop_name, area, weather, soil_quality)
            return JsonResponse({'success': True, 'prediction': result})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# ============ FERTILIZER ADVISOR ============
@login_required
def ai_fertilizer_advisor(request):
    """AI Fertilizer Recommendation API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            crop_name = data.get('crop', 'rice')
            soil_type = data.get('soil', 'loamy')
            growth_stage = data.get('stage', 'vegetative')
            
            result = ai_services.get_fertilizer_recommendation(crop_name, soil_type, growth_stage)
            return JsonResponse({'success': True, 'recommendation': result})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# ============ PEST PREDICTOR ============
@login_required
def ai_pest_predictor(request):
    """AI Pest Prediction API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            season = data.get('season', 'kharif')
            
            location = request.user.village or request.user.district or "Delhi"
            weather = weather_service.get_current_weather(location)
            
            result = ai_services.predict_pest_attack(weather, season)
            return JsonResponse({'success': True, 'prediction': result})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# ============ FARM ANALYSIS ============
@login_required
def ai_farm_analysis(request):
    """AI Farm Performance Analysis API"""
    try:
        from crops.models import FarmerCrop
        from farmmanager.models import Expense
        
        crops = FarmerCrop.objects.filter(farmer=request.user)
        expenses = Expense.objects.filter(farmer=request.user)
        
        location = request.user.village or request.user.district or "Delhi"
        weather_history = [weather_service.get_current_weather(location) for _ in range(7)]
        
        result = ai_services.analyze_farm_performance(crops, expenses, weather_history)
        return JsonResponse({'success': True, 'analysis': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})