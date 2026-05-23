from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Market, Price, PriceAlert
from crops.models import Crop
from .market_service import market_service
import json

@login_required
def market_dashboard(request):
    """Market dashboard with real-time prices"""
    crops = Crop.objects.all()
    markets = Market.objects.all()
    
    selected_crop = request.GET.get('crop')
    selected_market = request.GET.get('market')
    
    prices = []
    selected_crop_name = ""
    
    if selected_crop:
        crop_obj = get_object_or_404(Crop, id=selected_crop)
        selected_crop_name = crop_obj.name
        
        # Get real-time prices from service
        market_name = None
        if selected_market and selected_market != 'all':
            market_obj = get_object_or_404(Market, id=selected_market)
            market_name = market_obj.name
        
        prices = market_service.get_real_time_prices(selected_crop_name, market_name)
        
        # Save to database for history (optional)
        if prices:
            for price_data in prices:
                market, created = Market.objects.get_or_create(
                    name=price_data['market'],
                    defaults={'city': price_data['market'].split(',')[0] if ',' in price_data['market'] else price_data['market'], 'state': 'India'}
                )
                
                Price.objects.create(
                    crop=crop_obj,
                    market=market,
                    price_per_quintal=price_data['price'],
                    trend=price_data['trend']
                )
    
    context = {
        'crops': crops,
        'markets': markets,
        'prices': prices,
        'selected_crop': selected_crop,
        'selected_market': selected_market,
        'selected_crop_name': selected_crop_name,
        'last_updated': market_service.get_simulated_prices('rice')[0]['date'] if prices else 'Today',
    }
    return render(request, 'market/dashboard.html', context)

@login_required
def get_realtime_prices_api(request):
    """API endpoint for real-time price updates"""
    crop_name = request.GET.get('crop')
    market_name = request.GET.get('market')
    
    if not crop_name:
        return JsonResponse({'error': 'Crop name required'}, status=400)
    
    prices = market_service.get_real_time_prices(crop_name, market_name)
    
    return JsonResponse({
        'success': True,
        'prices': prices,
        'crop': crop_name,
        'updated_at': datetime.now().strftime('%I:%M %p')
    })

@login_required
def set_price_alert(request):
    """Set price alert for a crop"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.headers.get('Content-Type') == 'application/json' else request.POST
            crop_id = data.get('crop')
            target_price = data.get('target_price')
            
            crop = get_object_or_404(Crop, id=crop_id)
            
            alert, created = PriceAlert.objects.get_or_create(
                farmer=request.user,
                crop=crop,
                defaults={'target_price': target_price}
            )
            
            if not created:
                alert.target_price = target_price
                alert.is_active = True
                alert.save()
            
            return JsonResponse({'status': 'success', 'message': f'Alert set for {crop.name} at ₹{target_price}/quintal'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def check_alerts(request):
    """Check if any price alerts are triggered"""
    alerts = PriceAlert.objects.filter(farmer=request.user, is_active=True)
    triggered = []
    
    for alert in alerts:
        current_prices = market_service.get_real_time_prices(alert.crop.name)
        for price in current_prices:
            if price['price'] <= float(alert.target_price):
                triggered.append({
                    'crop': alert.crop.name,
                    'market': price['market'],
                    'current_price': price['price'],
                    'target_price': float(alert.target_price)
                })
    
    return JsonResponse({'triggered_alerts': triggered})

@login_required
def delete_alert(request, alert_id):
    """Delete a price alert"""
    alert = get_object_or_404(PriceAlert, id=alert_id, farmer=request.user)
    alert.delete()
    return JsonResponse({'status': 'success'})

@login_required
def my_alerts(request):
    """View user's price alerts"""
    alerts = PriceAlert.objects.filter(farmer=request.user, is_active=True)
    return render(request, 'market/my_alerts.html', {'alerts': alerts})