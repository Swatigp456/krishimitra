from django.contrib import admin
from .models import Market, Price, PriceAlert

admin.site.register(Market)
admin.site.register(Price)
admin.site.register(PriceAlert)