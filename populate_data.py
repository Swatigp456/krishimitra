# populate_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'krishimitra.settings')
django.setup()

from crops.models import Crop, CropAdvisory

def populate():
    print("Starting data population...")
    
    # Create crops
    crops_data = [
        {'name': 'Rice', 'name_hi': 'धान', 'season': 'kharif', 'sowing_period': 'June-July', 'harvesting_period': 'October-November'},
        {'name': 'Wheat', 'name_hi': 'गेहूं', 'season': 'rabi', 'sowing_period': 'November-December', 'harvesting_period': 'March-April'},
        {'name': 'Corn', 'name_hi': 'मक्का', 'season': 'kharif', 'sowing_period': 'June-July', 'harvesting_period': 'September-October'},
        {'name': 'Cotton', 'name_hi': 'कपास', 'season': 'kharif', 'sowing_period': 'May-June', 'harvesting_period': 'November-December'},
        {'name': 'Sugarcane', 'name_hi': 'गन्ना', 'season': 'zaid', 'sowing_period': 'February-March', 'harvesting_period': 'December-January'},
    ]
    
    created_crops = []
    for crop_data in crops_data:
        crop, created = Crop.objects.get_or_create(
            name=crop_data['name'],
            defaults=crop_data
        )
        created_crops.append(crop)
        print(f"{'Created' if created else 'Found'} crop: {crop.name}")
    
    # Create advisories for Rice
    rice = Crop.objects.get(name='Rice')
    rice_advisories = [
        {'stage': 'sowing', 'title': '🌾 Sowing Preparation for Rice', 'advice': 'Prepare nursery beds with well-decomposed FYM. Use certified seeds @ 40-50 kg/acre. Treat seeds with fungicide before sowing. Best time: June-July.', 'priority': 1},
        {'stage': 'germination', 'title': '🌱 Germination Care', 'advice': 'Keep nursery beds moist but not waterlogged. Apply light irrigation daily. Protect from birds. Germination takes 5-7 days.', 'priority': 2},
        {'stage': 'vegetative', 'title': '🍃 Vegetative Growth Management', 'advice': 'Maintain 5cm standing water. Apply first dose of nitrogen fertilizer @ 25kg/acre after 20-25 days. Remove weeds manually.', 'priority': 2},
        {'stage': 'flowering', 'title': '🌸 Flowering Stage Care', 'advice': 'Monitor for stem borer and leaf folder. Install light traps. Apply recommended pesticides if pest exceeds ETL. Maintain water level.', 'priority': 1},
        {'stage': 'harvesting', 'title': '🌾 Harvesting Tips', 'advice': 'Harvest when 80% grains are straw-colored. Moisture content should be 20-22% for harvesting. Use combine harvester for large fields.', 'priority': 1},
    ]
    
    for adv in rice_advisories:
        obj, created = CropAdvisory.objects.get_or_create(
            crop=rice,
            growth_stage=adv['stage'],
            defaults={
                'title': adv['title'],
                'advice': adv['advice'],
                'priority': adv['priority'],
                'weather_condition': 'normal'
            }
        )
        print(f"{'Created' if created else 'Found'} advisory: Rice - {adv['stage']}")
    
    # Create advisories for Wheat
    wheat = Crop.objects.get(name='Wheat')
    wheat_advisories = [
        {'stage': 'sowing', 'title': '🌾 Wheat Sowing Guide', 'advice': 'Treat seeds with fungicide @ 2g/kg seed. Use row spacing of 20-22cm. Seed rate 100-120 kg/acre. Best time: November-December.', 'priority': 1},
        {'stage': 'germination', 'title': '🌱 Germination Period', 'advice': 'Ensure proper soil moisture. First irrigation at 20-25 days after sowing. Germination takes 5-8 days.', 'priority': 2},
        {'stage': 'vegetative', 'title': '🍃 Vegetative Growth', 'advice': 'First irrigation at crown root initiation (20-25 DAS). Second irrigation at tillering stage. Apply nitrogen @ 35kg/acre.', 'priority': 2},
        {'stage': 'flowering', 'title': '🌸 Flowering Care', 'advice': 'Apply second dose of nitrogen @ 35kg/acre. Spray 2% urea solution if yellowing observed. Watch for rust disease.', 'priority': 1},
        {'stage': 'harvesting', 'title': '🌾 Harvesting Wheat', 'advice': 'Harvest when grains become hard and moisture content is 14-15%. Avoid delayed harvesting to reduce shattering. Use combine harvester.', 'priority': 1},
    ]
    
    for adv in wheat_advisories:
        obj, created = CropAdvisory.objects.get_or_create(
            crop=wheat,
            growth_stage=adv['stage'],
            defaults={
                'title': adv['title'],
                'advice': adv['advice'],
                'priority': adv['priority'],
                'weather_condition': 'normal'
            }
        )
        print(f"{'Created' if created else 'Found'} advisory: Wheat - {adv['stage']}")
    
    # Create advisories for Corn
    corn = Crop.objects.get(name='Corn')
    corn_advisories = [
        {'stage': 'sowing', 'title': '🌽 Corn Planting Guide', 'advice': 'Plow deeply and level field. Use row spacing 60x20cm. Seed rate 20-25 kg/acre. Best time: June-July.', 'priority': 1},
        {'stage': 'germination', 'title': '🌱 Corn Germination', 'advice': 'Keep soil moist. Germination takes 4-7 days. Apply pre-emergence herbicide for weed control.', 'priority': 2},
        {'stage': 'vegetative', 'title': '🍃 Corn Growth Stage', 'advice': 'Apply DAP @ 50kg/acre at sowing. Apply first dose of nitrogen @ 30kg/acre at knee-high stage. Irrigate weekly.', 'priority': 2},
        {'stage': 'flowering', 'title': '🌸 Corn Silking/Tasseling', 'advice': 'Monitor for fall armyworm. Install pheromone traps @ 5/acre. Spray emamectin benzoate if needed. Ensure adequate moisture.', 'priority': 1},
        {'stage': 'harvesting', 'title': '🌽 Harvesting Corn', 'advice': 'Harvest when husk turns yellow-brown. Moisture content should be 20-25% for harvesting. Dry grains to 14% moisture for storage.', 'priority': 1},
    ]
    
    for adv in corn_advisories:
        obj, created = CropAdvisory.objects.get_or_create(
            crop=corn,
            growth_stage=adv['stage'],
            defaults={
                'title': adv['title'],
                'advice': adv['advice'],
                'priority': adv['priority'],
                'weather_condition': 'normal'
            }
        )
        print(f"{'Created' if created else 'Found'} advisory: Corn - {adv['stage']}")
    
    print("\n" + "="*50)
    print("✅ DATA POPULATION COMPLETE!")
    print(f"Total Crops: {Crop.objects.count()}")
    print(f"Total Advisories: {CropAdvisory.objects.count()}")
    print("="*50)

if __name__ == '__main__':
    populate()