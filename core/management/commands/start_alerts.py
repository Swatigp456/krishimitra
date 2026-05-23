# core/management/commands/start_alerts.py
from django.core.management.base import BaseCommand
from core.tasks import scheduler

class Command(BaseCommand):
    help = 'Start weather alert background service'
    
    def handle(self, *args, **options):
        self.stdout.write('Starting weather alert service...')
        scheduler.start()
        self.stdout.write('✅ Weather alert service running!')
        
        # Keep running
        import time
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stdout.write('Stopping weather alert service...')
            scheduler.stop()