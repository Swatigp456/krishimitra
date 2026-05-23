from django.contrib import admin
from .models import Crop, CropAdvisory, FarmerCrop

admin.site.register(Crop)
admin.site.register(CropAdvisory)
admin.site.register(FarmerCrop)