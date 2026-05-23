# core/tasks.py
import threading
import time
from datetime import datetime, timedelta
from .weather_utils import weather_service
from .sms_service import sms_service

class WeatherAlertScheduler:
    """Background scheduler for weather alerts"""
    
    def __init__(self):
        self.running = True
        self.last_alert_time = {}
    
    def start(self):
        """Start the background scheduler"""
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()
        print("✅ Weather Alert Scheduler Started")
    
    def _run(self):
        """Run the scheduler loop"""
        while self.running:
            try:
                self.check_and_send_alerts()
                time.sleep(1800)  # Check every 30 minutes
            except Exception as e:
                print(f"Scheduler error: {e}")
                time.sleep(60)
    
    def check_and_send_alerts(self):
        """Check weather and send alerts to all farmers"""
        from core.models import Farmer
        
        farmers = Farmer.objects.filter(is_active=True)
        
        for farmer in farmers:
            try:
                # Get farmer's location
                location = farmer.village or farmer.district or "Delhi"
                
                # Get current weather
                weather = weather_service.get_current_weather(location)
                alerts = weather_service.get_weather_alerts(weather)
                
                # Check if we need to send SMS
                farmer_key = f"{farmer.id}_{datetime.now().strftime('%Y%m%d')}"
                
                for alert in alerts:
                    # Only send high-priority alerts (danger)
                    if alert['type'] in ['danger', 'warning']:
                        alert_key = f"{farmer_key}_{alert['title']}"
                        
                        # Don't send same alert more than once per day
                        if alert_key not in self.last_alert_time:
                            self.last_alert_time[alert_key] = datetime.now()
                            
                            # Send SMS
                            sms_service.send_weather_alert_sms(farmer, alert)
                            print(f"📱 SMS sent to {farmer.phone}: {alert['title']}")
                            
            except Exception as e:
                print(f"Error processing farmer {farmer.id}: {e}")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False

# Start scheduler when Django starts
scheduler = WeatherAlertScheduler()