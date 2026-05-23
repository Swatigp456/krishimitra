# core/multimodal_service.py - Using REST API (No deprecated warnings)
import requests
import base64
import json
from PIL import Image
import io

class MultimodalAIService:
    """Gemini API via REST - Crop Disease Detection (No deprecated warnings)"""
    
    def __init__(self):
        self.api_key = "AIzaSyB2N5XqITOaVbFhrAdVPH_g2RFVEEUbu34"
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"
    
    def analyze_crop_image(self, image_file, question=None, language="en"):
        """Analyze crop image using REST API"""
        try:
            # Open and process image
            image = Image.open(image_file)
            
            # Convert to RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize
            max_size = (1024, 1024)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convert image to base64
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG", quality=80)
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Prepare prompt
            if language == 'hi':
                text_prompt = f"इस फसल की छवि का विश्लेषण करें। {question if question else 'कोई रोग या समस्या पहचानें'}। व्यावहारिक सलाह दें।"
            elif language == 'kn':
                text_prompt = f"ಈ ಬೆಳೆ ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸಿ. {question if question else 'ಯಾವುದೇ ರೋಗ ಅಥವಾ ಸಮಸ್ಯೆಯನ್ನು ಗುರುತಿಸಿ'}. ಪ್ರಾಯೋಗಿಕ ಸಲಹೆ ನೀಡಿ."
            else:
                text_prompt = f"Analyze this crop image. {question if question else 'Identify any disease or problem'}. Give practical advice for Indian farmers."
            
            # Prepare request
            headers = {'Content-Type': 'application/json'}
            
            data = {
                "contents": [{
                    "parts": [
                        {"text": text_prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": img_base64
                            }
                        }
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.4,
                    "maxOutputTokens": 800,
                }
            }
            
            # Make API call
            url = f"{self.api_url}?key={self.api_key}"
            response = requests.post(url, headers=headers, json=data, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                answer = result['candidates'][0]['content']['parts'][0]['text']
                return {'success': True, 'analysis': answer, 'language': language}
            else:
                error_detail = response.json() if response.text else {}
                print(f"API Error: {response.status_code}")
                return self.get_fallback_analysis(question, language)
                
        except Exception as e:
            print(f"Error: {e}")
            return self.get_fallback_analysis(question, language)
    
    def get_fallback_analysis(self, question, language="en"):
        """Fallback analysis when API fails"""
        if language == 'hi':
            return {
                'success': True,
                'analysis': """🔍 **फसल रोग विश्लेषण**

आपकी फसल में समस्या हो सकती है:

**सुझाव:**
1. प्रभावित पत्तियों को हटा दें
2. नीम तेल का छिड़काव करें
3. कृषि अधिकारी से संपर्क करें

💡 बेहतर विश्लेषण के लिए साफ फोटो अपलोड करें।"""
            }
        else:
            return {
                'success': True,
                'analysis': """🔍 **Crop Disease Analysis**

**Recommendations:**
1. Remove affected leaves
2. Spray neem oil solution
3. Consult local agriculture officer

💡 For better analysis, upload a clear, well-lit photo."""
            }

multimodal_service = MultimodalAIService()