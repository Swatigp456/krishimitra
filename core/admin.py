from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Farmer, Location

class FarmerAdmin(UserAdmin):
    list_display = ['username', 'phone', 'village', 'district', 'created_at']
    search_fields = ['username', 'phone', 'village']
    fieldsets = UserAdmin.fieldsets + (
        ('Farmer Details', {'fields': ('phone', 'village', 'district', 'state', 'land_size', 'preferred_language', 'profile_picture')}),
    )

admin.site.register(Farmer, FarmerAdmin)
admin.site.register(Location)