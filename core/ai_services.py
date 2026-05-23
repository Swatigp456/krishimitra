# core/ai_services.py - Complete Working AI Services
import requests
import json

class AIServices:
    """AI Services for Farming Predictions"""
    
    def __init__(self):
        self.api_key = "AIzaSyB2N5XqITOaVbFhrAdVPH_g2RFVEEUbu34"
    
    # ============ DISEASE PREDICTOR ============
    def predict_disease_risk(self, crop_name, weather_data, growth_stage):
        """Predict disease risk based on weather and growth stage"""
        temp = weather_data.get('temp', 25)
        humidity = weather_data.get('humidity', 65)
        
        risk_score = 0
        risk_factors = []
        
        if temp > 35:
            risk_factors.append(f"⚠️ High temperature ({temp}°C) - Disease risk increases")
            risk_score += 40
        elif temp < 15:
            risk_factors.append(f"⚠️ Low temperature ({temp}°C) - Crop stress")
            risk_score += 30
        
        if humidity > 80:
            risk_factors.append(f"💧 High humidity ({humidity}%) - Fungal disease risk")
            risk_score += 40
        elif humidity < 40:
            risk_factors.append(f"🌵 Low humidity ({humidity}%) - Pest risk increases")
            risk_score += 20
        
        if growth_stage in ['flowering', 'fruiting']:
            risk_factors.append(f"🌸 {growth_stage} stage - Critical period, high vulnerability")
            risk_score += 30
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = "🔴 HIGH RISK"
            recommendation = "Take immediate action! Inspect crops daily. Apply preventive fungicides if needed."
        elif risk_score >= 40:
            risk_level = "🟡 MEDIUM RISK"
            recommendation = "Monitor crops closely. Keep field clean and ensure good air circulation."
        else:
            risk_level = "🟢 LOW RISK"
            recommendation = "Normal monitoring sufficient. Continue regular farming practices."
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'recommendation': recommendation
        }
    
    # ============ YIELD PREDICTOR ============
    def predict_yield(self, crop_name, area_acres, weather_data, soil_quality='medium'):
        """Predict crop yield based on crop, area, soil quality"""
        
        # Base yield per acre (quintals)
        base_yields = {
            'rice': 22,
            'wheat': 20,
            'corn': 25,
            'cotton': 8,
            'sugarcane': 350
        }
        
        base_yield = base_yields.get(crop_name.lower(), 20)
        
        # Soil quality factor
        soil_factors = {
            'poor': 0.7,
            'medium': 1.0,
            'good': 1.2
        }
        soil_factor = soil_factors.get(soil_quality, 1.0)
        
        # Weather impact (based on temperature)
        temp = weather_data.get('temp', 25)
        if 20 <= temp <= 30:
            weather_factor = 1.1
        elif temp > 35 or temp < 15:
            weather_factor = 0.8
        else:
            weather_factor = 0.95
        
        # Calculate predicted yield
        predicted_per_acre = base_yield * soil_factor * weather_factor
        predicted_total = predicted_per_acre * float(area_acres)
        confidence = min(95, int(85 * soil_factor * weather_factor))
        
        return {
            'predicted_yield_per_acre': round(predicted_per_acre, 1),
            'predicted_total_yield': round(predicted_total, 1),
            'confidence': confidence,
            'base_yield': base_yield,
            'factors': {
                'soil': round(soil_factor * 100, 0),
                'weather': round(weather_factor * 100, 0)
            },
            'recommendations': [
                "Use high-quality certified seeds",
                "Follow recommended fertilizer schedule",
                "Ensure proper irrigation",
                "Monitor for pests and diseases regularly"
            ]
        }
    
    # ============ FERTILIZER ADVISOR ============
    def get_fertilizer_recommendation(self, crop_name, soil_type='loamy', growth_stage='vegetative'):
        """Get fertilizer recommendations based on crop and growth stage"""
        
        recommendations = []
        
        if growth_stage == 'sowing':
            recommendations.append({
                'type': 'Basal Dose',
                'fertilizer': 'DAP (Diammonium Phosphate)',
                'quantity': '50-60 kg/acre',
                'timing': 'At the time of sowing',
                'method': 'Mix in soil during final plowing'
            })
            recommendations.append({
                'type': 'Organic',
                'fertilizer': 'Farm Yard Manure (FYM)',
                'quantity': '4-5 tons/acre',
                'timing': '15 days before sowing',
                'method': 'Spread evenly and mix in soil'
            })
            
        elif growth_stage == 'vegetative':
            recommendations.append({
                'type': 'Nitrogen Dose',
                'fertilizer': 'Urea',
                'quantity': '30-40 kg/acre',
                'timing': '20-25 days after sowing',
                'method': 'Apply near root zone and irrigate'
            })
            
        elif growth_stage == 'flowering':
            recommendations.append({
                'type': 'Potash + Micronutrients',
                'fertilizer': 'MOP + Zinc Sulphate',
                'quantity': '25 kg MOP + 10 kg Zinc/acre',
                'timing': 'At flowering stage',
                'method': 'Foliar spray or soil application'
            })
        
        # Soil-specific advice
        if soil_type == 'sandy':
            recommendations.append({
                'type': 'Soil Amendment',
                'advice': 'Sandy soil needs more organic matter. Add compost and use green manure for moisture retention.'
            })
        elif soil_type == 'clay':
            recommendations.append({
                'type': 'Soil Amendment',
                'advice': 'Clay soil needs gypsum to improve drainage. Avoid over-irrigation.'
            })
        
        return recommendations
    
    # ============ PEST PREDICTOR ============
    def predict_pest_attack(self, weather_data, season='kharif'):
        """Predict pest attack risk based on weather"""
        
        temp = weather_data.get('temp', 25)
        humidity = weather_data.get('humidity', 65)
        
        if temp > 32 and humidity < 50:
            return {
                'severity': 'High',
                'predicted_pests': ['Aphids', 'Thrips', 'Whitefly', 'Mites'],
                'action_required': '⚠️ Immediate action needed! Install yellow sticky traps. Spray neem oil solution (5ml/L) weekly.',
                'prevention_tips': [
                    '🔍 Inspect crops twice weekly',
                    '🚜 Maintain field hygiene',
                    '🌱 Use resistant varieties',
                    '🪤 Install pheromone traps'
                ]
            }
        elif humidity > 80 and temp < 28:
            return {
                'severity': 'High',
                'predicted_pests': ['Fungal Diseases', 'Leaf Blight', 'Powdery Mildew', 'Downy Mildew'],
                'action_required': '⚠️ High humidity promotes fungal diseases. Ensure good air circulation. Apply fungicide if needed.',
                'prevention_tips': [
                    '🌬️ Ensure proper plant spacing',
                    '💧 Avoid overhead irrigation',
                    '🍂 Remove infected leaves',
                    '🧪 Apply preventive fungicides'
                ]
            }
        elif season == 'kharif' and 'rain' in weather_data.get('condition', '').lower():
            return {
                'severity': 'Medium',
                'predicted_pests': ['Stem Borer', 'Leaf Folder', 'Rice Blast'],
                'action_required': '⚠️ Monitor daily. Use pheromone traps. Consult local agriculture officer.',
                'prevention_tips': [
                    '🪤 Install pheromone traps',
                    '🌾 Use resistant varieties',
                    '💨 Ensure air circulation',
                    '📊 Keep pest records'
                ]
            }
        else:
            return {
                'severity': 'Low',
                'predicted_pests': ['Minor pest activity expected'],
                'action_required': '✅ Regular monitoring is sufficient. No immediate action needed.',
                'prevention_tips': [
                    '🔍 Regular field inspection',
                    '🧹 Keep field clean',
                    '🌱 Healthy plants are less susceptible',
                    '📅 Plan preventive sprays'
                ]
            }
    
    # ============ FARM ANALYSIS ============
    def analyze_farm_performance(self, crops_data, expenses, weather_history):
        """Analyze overall farm performance"""
        
        total_expenses = sum(float(e.amount) for e in expenses) if expenses else 0
        total_area = sum(float(c.area) for c in crops_data) if crops_data else 0
        crop_count = len(crops_data)
        
        # Smart insights
        insights = []
        
        if total_expenses > 10000:
            insights.append("💰 Your expenses are high. Consider cost-saving measures like organic fertilizers.")
        elif total_expenses < 5000:
            insights.append("🎯 Excellent cost management! Keep tracking your expenses.")
        
        if crop_count >= 2:
            insights.append("✅ Good crop diversification! This reduces risk and improves soil health.")
        elif crop_count == 1:
            insights.append("⚠️ Consider diversifying your crops to reduce risk and increase income.")
        
        if total_area > 10:
            insights.append("📊 Large farm detected - consider mechanization for efficiency.")
        
        # Score calculation
        score = 70  # base score
        if crop_count >= 2:
            score += 10
        if total_expenses < 5000:
            score += 10
        if total_area > 0:
            score += 5
        
        # Recommendation
        if score >= 80:
            recommendation = "🌟 Excellent farm performance! Continue your good practices."
        elif score >= 60:
            recommendation = "👍 Good performance. Focus on cost optimization and crop diversification."
        else:
            recommendation = "📈 Your farm has potential. Consider reducing expenses and diversifying crops."
        
        return {
            'score': min(100, score),
            'insights': insights,
            'total_expenses': total_expenses,
            'total_area': total_area,
            'crop_count': crop_count,
            'recommendation': recommendation
        }

ai_services = AIServices()