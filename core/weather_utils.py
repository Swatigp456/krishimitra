import requests
from datetime import datetime, timedelta
from django.conf import settings

class WeatherService:
    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, city=None, state=None, country="IN"):
        """Get current weather for a location"""
        try:
            if city and city != "Unknown":
                location = f"{city},IN"
            else:
                location = "Delhi,IN"
            
            url = f"{self.base_url}/weather?q={location}&appid={self.api_key}&units=metric"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'temp': round(data['main']['temp']),
                    'feels_like': round(data['main']['feels_like']),
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'condition': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'wind_speed': data['wind']['speed'],
                    'city': data['name'],
                    'country': data['sys']['country']
                }
            else:
                return self.get_mock_weather(city)
        except Exception as e:
            print(f"Weather API error: {e}")
            return self.get_mock_weather(city)
    
    def get_forecast(self, city=None):
        """Get weather forecast for next days"""
        try:
            if city and city != "Unknown":
                location = f"{city},IN"
            else:
                location = "Delhi,IN"
                
            url = f"{self.base_url}/forecast?q={location}&appid={self.api_key}&units=metric"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                forecast_list = []
                
                for item in data['list'][:8]:
                    forecast_list.append({
                        'time': datetime.fromtimestamp(item['dt']).strftime('%I:%M %p'),
                        'date': datetime.fromtimestamp(item['dt']).strftime('%d %b'),
                        'temp': round(item['main']['temp']),
                        'condition': item['weather'][0]['description'],
                        'icon': item['weather'][0]['icon'],
                        'rain': item.get('rain', {}).get('3h', 0)
                    })
                
                return {
                    'success': True,
                    'forecast': forecast_list,
                    'city': data['city']['name']
                }
            else:
                return self.get_mock_forecast(city)
        except Exception as e:
            print(f"Forecast API error: {e}")
            return self.get_mock_forecast(city)
    
    def get_weather_alerts(self, weather_data):
        """Generate weather-based alerts for farmers"""
        alerts = []
        
        temp = weather_data.get('temp', 25)
        humidity = weather_data.get('humidity', 65)
        wind = weather_data.get('wind_speed', 10)
        condition = weather_data.get('condition', '').lower()
        
        # Temperature alerts
        if temp > 35:
            alerts.append({
                'type': 'danger',
                'title': '🔥 Heatwave Alert',
                'message': f'Temperature is {temp}°C. Irrigate crops immediately.',
                'action': 'Water crops in evening. Provide shade.'
            })
        elif temp > 30:
            alerts.append({
                'type': 'warning',
                'title': '🌡️ High Temperature Warning',
                'message': f'Temperature is {temp}°C. Monitor soil moisture.',
                'action': 'Check irrigation needs.'
            })
        elif temp < 10:
            alerts.append({
                'type': 'danger',
                'title': '❄️ Frost Alert',
                'message': f'Temperature dropped to {temp}°C. Cover sensitive crops.',
                'action': 'Use mulch or plastic covers.'
            })
        elif temp < 15:
            alerts.append({
                'type': 'warning',
                'title': '🌡️ Low Temperature Warning',
                'message': f'Temperature is {temp}°C. Protect young plants.',
                'action': 'Cover crops if possible.'
            })
        
        # Rain alerts
        if 'rain' in condition or 'thunderstorm' in condition:
            alerts.append({
                'type': 'warning',
                'title': '🌧️ Rain Expected',
                'message': 'Rain expected in your area today.',
                'action': 'Delay fertilizer application. Cover harvested crops.'
            })
        
        # Wind alerts
        if wind > 30:
            alerts.append({
                'type': 'warning',
                'title': '💨 Strong Wind Alert',
                'message': f'Wind speed {wind} km/h. Support tall crops.',
                'action': 'Secure farm structures. Support maize/sugarcane.'
            })
        
        # Humidity alerts
        if humidity > 80:
            alerts.append({
                'type': 'info',
                'title': '💧 High Humidity Alert',
                'message': f'Humidity at {humidity}%. Risk of fungal diseases.',
                'action': 'Monitor for diseases. Avoid irrigation.'
            })
        elif humidity < 30:
            alerts.append({
                'type': 'info',
                'title': '🌵 Low Humidity Alert',
                'message': f'Very dry conditions. Increase irrigation.',
                'action': 'Water crops more frequently.'
            })
        
        # Add a default alert if no alerts generated
        if len(alerts) == 0:
            alerts.append({
                'type': 'success',
                'title': '✅ Weather Conditions Normal',
                'message': 'Current weather is favorable for farming activities.',
                'action': 'Continue regular farming operations.'
            })
        
        return alerts
    
    def get_mock_weather(self, city="Unknown"):
        """Fallback mock data when API fails"""
        return {
            'success': True,
            'temp': 28,
            'feels_like': 27,
            'humidity': 65,
            'pressure': 1012,
            'condition': 'Partly cloudy',
            'icon': '02d',
            'wind_speed': 12,
            'city': city if city else 'Your Village',
            'country': 'IN'
        }
    
    def get_mock_forecast(self, city="Unknown"):
        """Fallback mock forecast data"""
        forecast = []
        now = datetime.now()
        for i in range(4):
            time_slot = now + timedelta(hours=i*3)
            forecast.append({
                'time': time_slot.strftime('%I:%M %p'),
                'date': time_slot.strftime('%d %b'),
                'temp': 28 - i,
                'condition': ['Clear', 'Partly cloudy', 'Clouds', 'Light rain'][i],
                'icon': ['01d', '02d', '03d', '10d'][i],
                'rain': [0, 0, 1, 3][i]
            })
        
        return {
            'success': True,
            'forecast': forecast,
            'city': city if city else 'Your Location'
        }

# Initialize weather service
weather_service = WeatherService()