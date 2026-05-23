from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import FarmerRegistrationForm, FarmerLoginForm
from .weather_utils import weather_service
from datetime import datetime
from .sms_service import sms_service
from .weather_utils import weather_service
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .multimodal_service import multimodal_service
import json



# ==================== HOME & AUTHENTICATION VIEWS ====================

def home(request):
    """Homepage view"""
    return render(request, 'core/home.html')

def register(request):
    """Farmer registration view"""
    if request.method == 'POST':
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to KrishiMitra.')
            return redirect('dashboard')
    else:
        form = FarmerRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    """User login view"""
    if request.method == 'POST':
        form = FarmerLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    else:
        form = FarmerLoginForm()
    return render(request, 'core/login.html', {'form': form})

def user_logout(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

# ==================== PROFILE VIEWS ====================

@login_required
def edit_profile(request):
    """Edit farmer profile - update location for accurate weather"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.village = request.POST.get('village', user.village)
        user.district = request.POST.get('district', user.district)
        user.state = request.POST.get('state', user.state)
        user.phone = request.POST.get('phone', user.phone)
        user.land_size = request.POST.get('land_size', user.land_size)
        user.save()
        messages.success(request, 'Profile updated successfully! Weather location updated.')
        return redirect('dashboard')
    
    return render(request, 'core/edit_profile.html', {'user': request.user})

# ==================== DASHBOARD VIEW ====================

@login_required
def dashboard(request):
    """Main dashboard with real-time weather, alerts, and recommendations"""
    
    # Get user's location from profile
    location = None
    if request.user.village and request.user.village != "":
        location = request.user.village
    elif request.user.district and request.user.district != "":
        location = request.user.district
    elif request.user.state and request.user.state != "":
        location = request.user.state
    else:
        location = "Delhi"
    
    # Get real-time weather data
    current_weather = weather_service.get_current_weather(location)
    forecast_data = weather_service.get_forecast(location)
    
    # Generate weather alerts based on current conditions
    weather_alerts = weather_service.get_weather_alerts(current_weather)
    
    # Get farmer's crops
    from crops.models import FarmerCrop
    farmer_crops = FarmerCrop.objects.filter(farmer=request.user)
    
    # Get crop-specific recommendations based on weather
    crop_recommendations = []
    temp = current_weather.get('temp', 25)
    
    for crop in farmer_crops[:3]:
        if crop.crop.name == 'Rice' and temp > 32:
            crop_recommendations.append(f'🌾 {crop.crop.name}: Increase water level due to high temperature')
        elif crop.crop.name == 'Wheat' and temp < 15:
            crop_recommendations.append(f'🌾 {crop.crop.name}: Provide frost protection')
        elif crop.crop.name == 'Corn' and temp > 35:
            crop_recommendations.append(f'🌽 {crop.crop.name}: Irrigate immediately - extreme heat')
        elif crop.crop.name == 'Cotton' and temp > 38:
            crop_recommendations.append(f'🌿 {crop.crop.name}: High temperature stress - avoid spraying')
    
    # Get government schemes
    from schemes.models import GovernmentScheme
    schemes = GovernmentScheme.objects.filter(is_active=True)[:3]
    
    # Get pending tasks from farm manager
    from farmmanager.models import FarmTask
    pending_tasks = FarmTask.objects.filter(farmer=request.user, is_completed=False)[:5]
    
    context = {
        'current_weather': current_weather,
        'forecast_data': forecast_data,
        'weather_alerts': weather_alerts,
        'farmer_crops': farmer_crops,
        'crop_recommendations': crop_recommendations,
        'schemes': schemes,
        'pending_tasks': pending_tasks,
        'current_time': datetime.now(),
        'farmer_location': location,
    }
    return render(request, 'core/dashboard.html', context)

# ==================== WEATHER API VIEW ====================

@login_required
def get_weather_api(request):
    """API endpoint for real-time weather updates without page reload"""
    
    # Get user's location
    if request.user.village and request.user.village != "":
        location = request.user.village
    elif request.user.district and request.user.district != "":
        location = request.user.district
    elif request.user.state and request.user.state != "":
        location = request.user.state
    else:
        location = request.GET.get('city', 'Delhi')
    
    # Get weather data
    current = weather_service.get_current_weather(location)
    forecast = weather_service.get_forecast(location)
    alerts = weather_service.get_weather_alerts(current)
    
    return JsonResponse({
        'success': True,
        'current': current,
        'forecast': forecast.get('forecast', []),
        'alerts': alerts,
        'location': location,
        'updated_at': datetime.now().strftime('%I:%M %p')
    })

# ==================== LANGUAGE SETTING VIEW ====================

def set_language(request):
    """Set user's preferred language"""
    if request.method == 'POST':
        lang = request.POST.get('language')
        if request.user.is_authenticated:
            request.user.preferred_language = lang
            request.user.save()
        request.session['django_language'] = lang
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

# ==================== PWA OFFLINE VIEW ====================

def offline_page(request):
    """Page shown when user is offline (PWA)"""
    return render(request, 'core/offline.html')

# ==================== SMART FARMING TOOLS VIEWS ====================

@login_required
def disease_detection(request):
    """AI Crop Disease Detection via Camera/Upload"""
    return render(request, 'crops/disease_detection.html')

@login_required
def fertilizer_calculator(request):
    """Smart Fertilizer Calculator"""
    return render(request, 'crops/fertilizer_calculator.html')

@login_required
def harvest_predictor(request):
    """Harvest Time Predictor"""
    from datetime import datetime, timedelta
    
    # Crop harvest days data
    crops_harvest_days = {
        'rice': {'min': 110, 'max': 130, 'ideal': 120},
        'wheat': {'min': 100, 'max': 120, 'ideal': 110},
        'corn': {'min': 90, 'max': 110, 'ideal': 100},
        'cotton': {'min': 140, 'max': 160, 'ideal': 150},
        'sugarcane': {'min': 300, 'max': 365, 'ideal': 330},
        'potato': {'min': 70, 'max': 90, 'ideal': 80},
        'tomato': {'min': 60, 'max': 80, 'ideal': 70},
    }
    
    prediction = None
    
    if request.method == 'POST':
        crop = request.POST.get('crop')
        sowing_date = request.POST.get('sowing_date')
        
        if crop and sowing_date:
            sowing = datetime.strptime(sowing_date, '%Y-%m-%d')
            days = crops_harvest_days.get(crop, {'min': 90, 'max': 110, 'ideal': 100})
            
            min_harvest = sowing + timedelta(days=days['min'])
            ideal_harvest = sowing + timedelta(days=days['ideal'])
            max_harvest = sowing + timedelta(days=days['max'])
            
            days_passed = (datetime.now() - sowing).days
            progress = min(100, int((days_passed / days['ideal']) * 100))
            days_remaining = max(0, days['ideal'] - days_passed)
            
            prediction = {
                'crop': crop,
                'sowing_date': sowing_date,
                'min_harvest': min_harvest.strftime('%d %B %Y'),
                'ideal_harvest': ideal_harvest.strftime('%d %B %Y'),
                'max_harvest': max_harvest.strftime('%d %B %Y'),
                'days_passed': days_passed,
                'days_remaining': days_remaining,
                'progress': progress,
            }
    
    return render(request, 'crops/harvest_predictor.html', {'prediction': prediction})

@login_required
def nearby_services(request):
    """Nearby agricultural services locator"""
    return render(request, 'core/nearby_services.html')

@login_required
def test_sms(request):
    """Test SMS functionality"""
    if request.method == 'POST':
        alert = {
            'title': 'Test Alert',
            'message': 'This is a test message from KrishiMitra',
            'action': 'Test action'
        }
        result = sms_service.send_weather_alert_sms(request.user, alert)
        if result:
            return JsonResponse({'status': 'success', 'message': 'SMS sent successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to send SMS'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

# Add this function to manually trigger weather alerts
@login_required
def trigger_weather_alert(request):
    """Manually trigger weather alert SMS"""
    location = request.user.village or request.user.district or "Delhi"
    weather = weather_service.get_current_weather(location)
    alerts = weather_service.get_weather_alerts(weather)
    
    if alerts:
        for alert in alerts:
            if alert['type'] in ['danger', 'warning']:
                sms_service.send_weather_alert_sms(request.user, alert)
                return JsonResponse({
                    'status': 'success',
                    'message': f"Alert sent: {alert['title']}",
                    'alert': alert
                })
    
    return JsonResponse({'status': 'info', 'message': 'No severe weather alerts at this time'})

# Add this function to check weather status via API (for external monitoring)
def weather_status_api(request):
    """API endpoint for external weather monitoring"""
    farmer_id = request.GET.get('farmer_id')
    if farmer_id:
        from core.models import Farmer
        try:
            farmer = Farmer.objects.get(id=farmer_id)
            location = farmer.village or farmer.district or "Delhi"
        except:
            location = "Delhi"
    else:
        location = request.GET.get('location', 'Delhi')
    
    weather = weather_service.get_current_weather(location)
    alerts = weather_service.get_weather_alerts(weather)
    
    return JsonResponse({
        'success': True,
        'location': location,
        'weather': weather,
        'alerts': alerts,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
# Add this function to core/views.py

@login_required
def switch_language(request):
    """Switch website language"""
    if request.method == 'POST':
        lang = request.POST.get('language')
        if lang in ['en', 'hi', 'kn']:
            request.user.preferred_language = lang
            request.user.save()
            request.session['django_language'] = lang
            
            # Activate language
            from django.utils import translation
            translation.activate(lang)
            
            messages.success(request, f'Language changed to {lang.upper()}')
    
    # Redirect back to previous page
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url)
@login_required
def switch_language(request):
    """Switch website language - persists across all pages"""
    if request.method == 'POST':
        lang = request.POST.get('language')
        if lang in ['en', 'hi', 'kn']:
            # Save to user profile (if logged in)
            request.user.preferred_language = lang
            request.user.save()
            
            # Save to session
            request.session['django_language'] = lang
            
            # Activate language
            from django.utils import translation
            translation.activate(lang)
            
            messages.success(request, f'Language changed to {lang.upper()}')
    
    # Redirect back to same page
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url)
@login_required
def multimodal_analysis(request):
    """Analyze crop image with AI"""
    if request.method == 'POST':
        try:
            image_file = request.FILES.get('image')
            question = request.POST.get('question', '')
            language = request.POST.get('language', 'en')
            
            if not image_file:
                return JsonResponse({'success': False, 'error': 'No image provided'})
            
            result = multimodal_service.analyze_crop_image(image_file, question, language)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def get_voice_assistant(request):
    """Voice assistant page with multimodal support"""
    return render(request, 'core/voice_assistant.html')
# core/ai_views.py - Update the ai_chat function

@login_required
def ai_chat(request):
    """AI Chatbot - Answers in selected language"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '')
            language = data.get('language', 'en')  # Get language from request
            
            # Pass language to ai_services
            response = ai_services.get_answer(query, language)
            return JsonResponse({'success': True, 'response': response})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})