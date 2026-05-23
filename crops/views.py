from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Crop, CropAdvisory, FarmerCrop
from .forms import FarmerCropForm

@login_required
def crop_advisory(request):
    # Get all crops from database
    crops = Crop.objects.all()
    
    # Get selected values from request
    selected_crop_id = request.GET.get('crop')
    growth_stage = request.GET.get('stage', 'vegetative')
    
    advisory = None
    selected_crop = None
    selected_crop_name = ""
    
    # Process if crop is selected
    if selected_crop_id and selected_crop_id != 'other' and selected_crop_id != '':
        try:
            selected_crop = Crop.objects.get(id=selected_crop_id)
            selected_crop_name = selected_crop.name
            # Get advisory for selected crop and stage
            advisory = CropAdvisory.objects.filter(
                crop=selected_crop, 
                growth_stage=growth_stage
            )
            print(f"Found {advisory.count()} advisories for {selected_crop_name} - {growth_stage}")  # Debug
        except Crop.DoesNotExist:
            selected_crop_id = None
    
    context = {
        'crops': crops,
        'selected_crop_id': selected_crop_id,
        'selected_crop_name': selected_crop_name,
        'advisory': advisory,
        'growth_stage': growth_stage,
    }
    return render(request, 'crops/advisory.html', context)

@login_required
def my_crops(request):
    farmer_crops = FarmerCrop.objects.filter(farmer=request.user)
    
    if request.method == 'POST':
        form = FarmerCropForm(request.POST)
        if form.is_valid():
            farmer_crop = form.save(commit=False)
            farmer_crop.farmer = request.user
            farmer_crop.save()
            return redirect('my_crops')
    else:
        form = FarmerCropForm()
    
    return render(request, 'crops/my_crops.html', {
        'farmer_crops': farmer_crops,
        'form': form
    })

def get_advisory_api(request):
    crop_id = request.GET.get('crop')
    stage = request.GET.get('stage', 'vegetative')
    
    advisories = CropAdvisory.objects.filter(crop_id=crop_id, growth_stage=stage)
    data = [{
        'title': a.title,
        'advice': a.advice,
        'priority': a.priority
    } for a in advisories]
    
    return JsonResponse({'advisories': data})

@login_required
def harvest_predictor(request):
    """Predict best harvest time based on crop and sowing date"""
    from datetime import datetime, timedelta
    import math
    
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
            
            # Weather check (mock)
            weather_good = True
            
            prediction = {
                'crop': crop,
                'sowing_date': sowing_date,
                'min_harvest': min_harvest.strftime('%d %B %Y'),
                'ideal_harvest': ideal_harvest.strftime('%d %B %Y'),
                'max_harvest': max_harvest.strftime('%d %B %Y'),
                'days_passed': days_passed,
                'days_remaining': max(0, days['ideal'] - days_passed),
                'progress': progress,
                'weather_good': weather_good
            }
    
    return render(request, 'crops/harvest_predictor.html', {'prediction': prediction})