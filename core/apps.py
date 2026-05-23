from django.apps import AppConfig
import threading
import time

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        """Start background scheduler for SMS alerts when Django starts"""
        
        # Start scheduler in background thread
        def start_background_scheduler():
            # Wait for Django to fully load
            time.sleep(5)
            
            try:
                from .tasks import scheduler
                scheduler.start()
                print("✅ Weather Alert SMS Scheduler Started Successfully")
            except Exception as e:
                print(f"⚠️ SMS Scheduler could not start: {e}")
                print("   SMS notifications will not work until you:")
                print("   1. Install required packages: pip install twilio requests")
                print("   2. Configure SMS API key in settings.py")
        
        # Start the scheduler in a daemon thread
        thread = threading.Thread(target=start_background_scheduler, daemon=True)
        thread.start()