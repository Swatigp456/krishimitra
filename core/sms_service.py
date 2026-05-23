# core/sms_service.py
import requests
from django.conf import settings

class SMSService:
    """SMS notification service for weather alerts"""
    
    def __init__(self):
        # Using free TextLocal API (works in India)
        # Sign up at https://textlocal.in for free API key (100 SMS/day free)
        self.api_key = "YOUR_TEXTLOCAL_API_KEY"  # Replace with your key
        self.sender = "KRISHI"  # Sender ID (6 characters max)
        self.api_url = "https://api.textlocal.in/send/"
    
    def send_sms(self, phone_number, message):
        """Send SMS to farmer"""
        try:
            # Clean phone number (remove +91 if present)
            phone = phone_number.replace('+', '').replace('91', '', 1) if phone_number.startswith('+') else phone_number
            
            params = {
                'apikey': self.api_key,
                'numbers': phone,
                'sender': self.sender,
                'message': message
            }
            
            response = requests.post(self.api_url, data=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('status') == 'success'
            return False
        except Exception as e:
            print(f"SMS error: {e}")
            return False
    
    def send_weather_alert_sms(self, farmer, alert):
        """Send weather alert SMS to farmer"""
        message = f"""🌾 KrishiMitra Weather Alert
        
📍 Location: {farmer.village or farmer.district}
⚠️ {alert['title']}
{alert['message']}
💡 {alert['action']}

- KrishiMitra Team"""
        
        return self.send_sms(farmer.phone, message)
    
    def send_price_alert_sms(self, farmer, crop, price, market):
        """Send price alert SMS to farmer"""
        message = f"""💰 KrishiMitra Price Alert
        
🌾 {crop} price at {market} market: ₹{price}/quintal
📉 Price dropped below your target!

Check app for more details.
- KrishiMitra Team"""
        
        return self.send_sms(farmer.phone, message)

# Initialize SMS service
sms_service = SMSService()