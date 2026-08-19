"""
Agricultural Demand Prediction - Flask API Server
Provides REST APIs for crop recommendation, fertilizer guidance,
price prediction, disease detection, and government schemes.
"""
import os
import sys
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.crop_recommendation import CropRecommender
from models.fertilizer_recommendation import FertilizerRecommender
from models.price_prediction import PricePredictor
from models.disease_detection import DiseaseDetector
from models.demand_supply import DemandSupplyAnalyzer
from models.profitability_calculator import ProfitabilityCalculator
from models.weather_advisory import WeatherAdvisoryEngine

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# ── Initialize Models ─────────────────────────────────────────────────────────
print("🌾 Initializing Agricultural AI Models...")

crop_recommender = CropRecommender()
fertilizer_recommender = FertilizerRecommender()
price_predictor = PricePredictor()
disease_detector = DiseaseDetector()
demand_supply_analyzer = DemandSupplyAnalyzer()
profitability_calculator = ProfitabilityCalculator()
weather_advisory_engine = WeatherAdvisoryEngine()

print("✅ All models initialized!")


# ── Serve Frontend ────────────────────────────────────────────────────────────
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)


# ── API: Health Check ─────────────────────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'models': {
            'crop_recommendation': crop_recommender.model is not None or 'ready',
            'fertilizer_recommendation': fertilizer_recommender.model is not None or 'ready',
            'price_prediction': price_predictor.model is not None or 'ready',
            'disease_detection': 'ready',
            'demand_supply_analyzer': 'ready',
            'profitability_calculator': 'ready',
            'weather_advisory': 'ready'
        }
    })


# ── API: Demand-Supply Glut Risk ─────────────────────────────────────────────
@app.route('/api/demand-supply-risk', methods=['POST'])
def demand_supply_risk():
    try:
        data = request.json or {}
        crop = data.get('crop', 'Rice')
        state = data.get('state', 'Karnataka')
        
        result = demand_supply_analyzer.analyze_risk(crop=crop, state=state)
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── API: Crop Profitability & Net ROI Calculator ─────────────────────────────
@app.route('/api/calculate-roi', methods=['POST'])
def calculate_roi():
    try:
        data = request.json or {}
        crop = data.get('crop', 'Rice')
        acres = data.get('acres', 1.0)
        price_per_qtl = data.get('price_per_qtl', None)
        
        result = profitability_calculator.calculate(crop=crop, acres=acres, price_per_qtl=price_per_qtl)
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── API: Smart Weather Advisory ───────────────────────────────────────────────
@app.route('/api/weather-advisory', methods=['GET'])
def weather_advisory():
    try:
        state = request.args.get('state', 'Karnataka')
        result = weather_advisory_engine.get_advisory(state=state)
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── API: Crop Recommendation ─────────────────────────────────────────────────
@app.route('/api/predict-crop', methods=['POST'])
def predict_crop():
    try:
        data = request.json
        required = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        
        for field in required:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        result = crop_recommender.predict(
            n=float(data['N']),
            p=float(data['P']),
            k=float(data['K']),
            temperature=float(data['temperature']),
            humidity=float(data['humidity']),
            ph=float(data['ph']),
            rainfall=float(data['rainfall'])
        )
        
        return jsonify({
            'success': True,
            'recommendations': result,
            'input_params': data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── API: Fertilizer Recommendation ───────────────────────────────────────────
@app.route('/api/recommend-fertilizer', methods=['POST'])
def recommend_fertilizer():
    try:
        data = request.json
        required = ['temperature', 'humidity', 'moisture', 'soil_type',
                     'crop_type', 'nitrogen', 'phosphorous', 'potassium']
        
        for field in required:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        result = fertilizer_recommender.predict(
            temperature=float(data['temperature']),
            humidity=float(data['humidity']),
            moisture=float(data['moisture']),
            soil_type=data['soil_type'],
            crop_type=data['crop_type'],
            nitrogen=float(data['nitrogen']),
            phosphorous=float(data['phosphorous']),
            potassium=float(data['potassium'])
        )
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/fertilizer-options', methods=['GET'])
def fertilizer_options():
    return jsonify({
        'soil_types': fertilizer_recommender.get_soil_types(),
        'crop_types': fertilizer_recommender.get_crop_types()
    })


# ── API: Price Prediction ────────────────────────────────────────────────────
@app.route('/api/predict-price', methods=['POST'])
def predict_price():
    try:
        data = request.json
        commodity = data.get('commodity', 'Rice')
        state = data.get('state', 'Karnataka')
        days = int(data.get('days', 30))
        days = min(days, 90)  # Cap at 90 days
        
        result = price_predictor.predict_future(commodity, state, days)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 400
        
        return jsonify({
            'success': True,
            'forecast': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/historical-prices', methods=['GET'])
def historical_prices():
    try:
        commodity = request.args.get('commodity', 'Rice')
        state = request.args.get('state', 'Karnataka')
        days = int(request.args.get('days', 90))
        
        result = price_predictor.get_historical(commodity, state, days)
        
        return jsonify({
            'success': True,
            'data': result,
            'commodity': commodity,
            'state': state
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/price-options', methods=['GET'])
def price_options():
    return jsonify({
        'commodities': price_predictor.get_commodities(),
        'states': price_predictor.get_states()
    })


# ── API: Disease Detection ───────────────────────────────────────────────────
@app.route('/api/detect-disease', methods=['POST'])
def detect_disease():
    try:
        if 'image' in request.files:
            image_file = request.files['image']
            filename = image_file.filename
            image_data = image_file.read()
        else:
            filename = request.json.get('filename', 'unknown.jpg') if request.json else 'unknown.jpg'
            image_data = None
        
        result = disease_detector.detect(image_data=image_data, filename=filename)
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/diseases', methods=['GET'])
def list_diseases():
    return jsonify({
        'diseases': disease_detector.get_all_diseases()
    })


# ── API: Government Schemes ──────────────────────────────────────────────────
@app.route('/api/schemes', methods=['GET'])
def get_schemes():
    try:
        schemes_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'data', 'government_schemes.json'
        )
        
        if os.path.exists(schemes_path):
            with open(schemes_path, 'r') as f:
                schemes = json.load(f)
        else:
            schemes = []
        
        category = request.args.get('category', None)
        if category:
            schemes = [s for s in schemes if s.get('category', '').lower() == category.lower()]
        
        return jsonify({
            'success': True,
            'schemes': schemes,
            'total': len(schemes)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── API: Nearby Markets (simulated with known markets) ───────────────────────
@app.route('/api/nearby-markets', methods=['POST'])
def nearby_markets():
    try:
        data = request.json
        lat = float(data.get('latitude', 12.97))
        lng = float(data.get('longitude', 77.59))
        
        # Simulated market database with GPS coordinates
        markets = [
            {"name": "APMC Yeshwanthpur", "lat": 13.0234, "lng": 77.5436, "state": "Karnataka", "commodities": ["Rice", "Wheat", "Vegetables"], "type": "Wholesale"},
            {"name": "KR Market Bangalore", "lat": 12.9636, "lng": 77.5779, "state": "Karnataka", "commodities": ["Fruits", "Vegetables", "Flowers"], "type": "Retail"},
            {"name": "Mandya APMC", "lat": 12.5218, "lng": 76.8952, "state": "Karnataka", "commodities": ["Sugarcane", "Rice", "Coconut"], "type": "Wholesale"},
            {"name": "Mysore APMC", "lat": 12.3051, "lng": 76.6551, "state": "Karnataka", "commodities": ["Tobacco", "Cotton", "Groundnut"], "type": "Wholesale"},
            {"name": "Hubli-Dharwad APMC", "lat": 15.3647, "lng": 75.1240, "state": "Karnataka", "commodities": ["Cotton", "Maize", "Soybean"], "type": "Wholesale"},
            {"name": "Shimoga APMC", "lat": 13.9299, "lng": 75.5681, "state": "Karnataka", "commodities": ["Areca nut", "Rice", "Pepper"], "type": "Wholesale"},
            {"name": "Raichur APMC", "lat": 16.2076, "lng": 77.3463, "state": "Karnataka", "commodities": ["Rice", "Cotton", "Sunflower"], "type": "Wholesale"},
            {"name": "Belgaum APMC", "lat": 15.8497, "lng": 74.4977, "state": "Karnataka", "commodities": ["Sugarcane", "Tobacco", "Jaggery"], "type": "Wholesale"},
            {"name": "Hassan APMC", "lat": 13.0073, "lng": 76.0962, "state": "Karnataka", "commodities": ["Coffee", "Pepper", "Coconut"], "type": "Wholesale"},
            {"name": "Tumkur APMC", "lat": 13.3379, "lng": 77.1010, "state": "Karnataka", "commodities": ["Coconut", "Groundnut", "Ragi"], "type": "Wholesale"},
            {"name": "Pune APMC", "lat": 18.5204, "lng": 73.8567, "state": "Maharashtra", "commodities": ["Onion", "Tomato", "Grapes"], "type": "Wholesale"},
            {"name": "Nashik APMC", "lat": 20.0063, "lng": 73.7903, "state": "Maharashtra", "commodities": ["Onion", "Grapes", "Pomegranate"], "type": "Wholesale"},
        ]
        
        import math
        
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = (math.sin(dlat/2)**2 +
                 math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
                 math.sin(dlon/2)**2)
            return R * 2 * math.asin(math.sqrt(a))
        
        for market in markets:
            market['distance_km'] = round(haversine(lat, lng, market['lat'], market['lng']), 1)
        
        markets.sort(key=lambda x: x['distance_km'])
        
        return jsonify({
            'success': True,
            'markets': markets[:8],
            'user_location': {'latitude': lat, 'longitude': lng}
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Chatbot helpers ───────────────────────────────────────────────────────────
FERTILIZER_PRICES = {
    'Urea': {'price': '₹266.50', 'unit': '45 kg bag', 'details': 'Statutory control price set by Government of India.'},
    'DAP (Diammonium Phosphate)': {'price': '₹1,350.00', 'unit': '50 kg bag', 'details': 'Highly subsidized phosphatic fertilizer.'},
    'MOP (Muriate of Potash)': {'price': '₹1,700.00', 'unit': '50 kg bag', 'details': 'Imported potassic fertilizer.'},
    'NPK 20-20-20': {'price': '₹1,400.00', 'unit': '50 kg bag', 'details': 'Balanced complex fertilizer for overall growth.'},
    'Balanced NPK 10-10-10': {'price': '₹1,100.00', 'unit': '50 kg bag', 'details': 'Maintenance grade complex fertilizer.'},
    'SSP (Single Super Phosphate)': {'price': '₹450.00', 'unit': '50 kg bag', 'details': 'Source of Phosphate, Calcium, and Sulfur.'}
}

CROP_FERTILIZER_GUIDE = {
    'Rice': {
        'fertilizer': 'Urea + DAP',
        'why': 'Rice requires high Nitrogen for vegetative growth and Phosphorous for root development.',
        'usage': 'Apply DAP as a basal dose at sowing (100 kg/ha) and Urea in 3 split doses (top-dressing).',
        'tips': 'Maintain shallow standing water during growth stages.'
    },
    'Wheat': {
        'fertilizer': 'Urea + DAP',
        'why': 'Wheat needs balanced nitrogen and phosphorus for tillering and grain filling.',
        'usage': 'DAP 100 kg/ha during sowing, followed by Urea 150 kg/ha after the first irrigation.',
        'tips': 'Irrigate at crown root initiation stage.'
    },
    'Maize': {
        'fertilizer': 'NPK 20-20-20 + Urea',
        'why': 'Maize is a heavy nutrient feeder, requiring balanced macro-nutrients.',
        'usage': 'Apply NPK 20-20-20 at sowing, and Urea at knee-high and silking stages.',
        'tips': 'Avoid water logging in early stages.'
    },
    'Cotton': {
        'fertilizer': 'Urea + MOP',
        'why': 'Cotton needs Nitrogen for boll development and Potash for fiber quality and strength.',
        'usage': 'Urea split doses (150 kg/ha total) and MOP (80 kg/ha) at square formation.',
        'tips': 'Monitor for sucking pests regularly.'
    },
    'Sugarcane': {
        'fertilizer': 'Urea + MOP',
        'why': 'Sugarcane requires immense vegetative growth, which demands high Nitrogen and Potassium.',
        'usage': 'Urea 250 kg/ha split over 3 months, MOP 120 kg/ha during earthing up.',
        'tips': 'Keep soil moist, irrigate every 10-15 days.'
    },
    'Coffee': {
        'fertilizer': 'NPK 20-20-20',
        'why': 'Coffee needs a balanced NPK ratio to maintain soil health and support berry growth.',
        'usage': 'Apply in two split doses: pre-monsoon (May) and post-monsoon (October).',
        'tips': 'Grow under regulated shade trees.'
    },
    'Coconut': {
        'fertilizer': 'MOP (Muriate of Potash)',
        'why': 'Coconut palms have a high demand for chlorine and potassium to improve nut yield.',
        'usage': 'Apply MOP 1.5 kg per palm per year along with organic manure.',
        'tips': 'Apply fertilizer in a basin around the palm (1.8m radius).'
    },
    'Groundnut': {
        'fertilizer': 'SSP (Single Super Phosphate)',
        'why': 'Groundnuts require calcium and sulfur for pegging and pod development.',
        'usage': 'SSP 250 kg/ha as a basal application during sowing.',
        'tips': 'Gypsum application at 45 days is crucial for pod filling.'
    },
    'Banana': {
        'fertilizer': 'MOP + Urea',
        'why': 'Banana is a heavy potassium consumer, essential for fruit size and sweetness.',
        'usage': 'Urea (200g/plant) and MOP (300g/plant) split into 4 doses during growth.',
        'tips': 'Keep the area weed-free and mulch heavily.'
    },
    'Mango': {
        'fertilizer': 'Balanced NPK 10-10-10',
        'why': 'Fruit trees need steady feeding. Nitrogen supports vegetative flush, Phosphorus supports flowering.',
        'usage': 'Apply 1-2 kg NPK per mature tree after harvest (June-July).',
        'tips': 'Prune dead wood after harvest to encourage new growth.'
    }
}

CHAT_TRANSLATIONS = {
    'en': {
        'greet': "Hello! I am your Hanu Agri Assistant. How can I help you today? You can ask me about crop prices, fertilizer rates, weather reports, or fertilizer recommendations.",
        'weather_prompt': "Which city would you like the weather report for? (e.g., weather in Bangalore)",
        'weather_err': "Sorry, I couldn't fetch the weather for {query}. Please try another city.",
        'crop_price_err': "Sorry, I couldn't find price data for {commodity} in {state}.",
        'crop_price_prompt': "Which crop price are you looking for? (e.g., price of Rice)",
        'fert_guide_prompt': "Which plant or crop are you looking for fertilizer recommendations for? (e.g., fertilizer for Wheat)",
        'fert_guide_err': "Sorry, I don't have fertilizer guidance for {crop} yet. Try Rice, Wheat, Cotton, Sugarcane, or Coconut.",
        'default': "I'm not sure I understand that. You can choose one of the options below or ask me about weather, crop prices, or fertilizers!"
    },
    'kn': {
        'greet': "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಅಗ್ರಿ-ಎಐ ಸಹಾಯಕ. ಇಂದು ನಿಮಗೆ ನಾನು ಹೇಗೆ ಸಹಾಯ ಮಾಡಲಿ? ನೀವು ಬೆಳೆ ಬೆಲೆಗಳು, ರಸಗೊಬ್ಬರ ದರಗಳು, ಹವಾಮಾನ ವರದಿ ಅಥವಾ ರಸಗೊಬ್ಬರ ಶಿಫಾರಸುಗಳ ಬಗ್ಗೆ ಕೇಳಬಹುದು.",
        'weather_prompt': "ಯಾವ ನಗರದ ಹವಾಮಾನ ವರದಿ ಬೇಕು? (ಉದಾಹರಣೆಗೆ: ಬೆಂಗಳೂರಿನ ಹವಾಮಾನ)",
        'weather_err': "ಕ್ಷಮಿಸಿ, {query} ಗಾಗಿ ಹವಾಮಾನ ಮಾಹಿತಿ ಪಡೆಯಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಬೇರೆ ನಗರ ಪ್ರಯತ್ನಿಸಿ.",
        'crop_price_err': "ಕ್ಷಮಿಸಿ, {state} ನಲ್ಲಿ {commodity} ಗಾಗಿ ಬೆಲೆ ಮಾಹಿತಿ ಸಿಗಲಿಲ್ಲ.",
        'crop_price_prompt': "ಯಾವ ಬೆಳೆಯ ಬೆಲೆಯನ್ನು ಹುಡುಕುತ್ತಿದ್ದೀರಾ? (ಉದಾಹರಣೆಗೆ: ಭತ್ತದ ಬೆಲೆ)",
        'fert_guide_prompt': "ಯಾವ ಬೆಳೆಗೆ ರಸಗೊಬ್ಬರ ಶಿಫಾರಸು ಬೇಕು? (ಉದಾಹರಣೆಗೆ: ಗೋಧಿಗೆ ರಸಗೊಬ್ಬರ)",
        'fert_guide_err': "ಕ್ಷಮಿಸಿ, {crop} ಬೆಳೆಗೆ ನನ್ನ ಬಳಿ ರಸಗೊಬ್ಬರ ಮಾಹಿತಿ ಇಲ್ಲ. ಭತ್ತ, ಗೋಧಿ, ಹತ್ತಿ, ಕಬ್ಬು ಅಥವಾ ತೆಂಗಿನಕಾಯಿ ಪ್ರಯತ್ನಿಸಿ.",
        'default': "ನಮಗೆ ಅದು ಅರ್ಥವಾಗುತ್ತಿಲ್ಲ. ಕೆಳಗಿನ ಆಯ್ಕೆಗಳಲ್ಲಿ ಒಂದನ್ನು ಆರಿಸಿ ಅಥವಾ ಹವಾಮಾನ, ಬೆಳೆ ಬೆಲೆಗಳು ಅಥವಾ ರಸಗೊಬ್ಬರಗಳ ಬಗ್ಗೆ ಕೇಳಿ!"
    },
    'hi': {
        'greet': "नमस्कार! मैं आपका एग्री-एआई सहायक हूँ। आज मैं आपकी क्या सहायता कर सकता हूँ? आप मुझसे फसल की कीमतों, उर्वरक दरों, मौसम की रिपोर्ट या उर्वरक सिफारिशों के बारे में पूछ सकते हैं।",
        'weather_prompt': "आप किस शहर की मौसम रिपोर्ट चाहते हैं? (जैसे, बैंगलोर में मौसम)",
        'weather_err': "क्षमा करें, मैं {query} के लिए मौसम की जानकारी नहीं ला सका। कृपया दूसरा शहर आज़माएँ.",
        'crop_price_err': "क्षमा करें, मुझे {state} में {commodity} के लिए कीमत का डेटा नहीं मिला।",
        'crop_price_prompt': "आप किस फसल की कीमत ढूंढ रहे हैं? (जैसे, चावल की कीमत)",
        'fert_guide_prompt': "आप किस फसल के लिए उर्वरक सिफारिशों की तलाश कर रहे हैं? (जैसे, गेहूं के लिए उर्वरक)",
        'fert_guide_err': "क्षमा करें, मेरे पास अभी {crop} के लिए उर्वरक मार्गदर्शन नहीं है। चावल, गेहूं, कपास, गन्ना या नारियल आज़माएं।",
        'default': "मुझे समझ नहीं आया। आप नीचे दिए गए विकल्पों में से चुन सकते हैं या मौसम, फसल की कीमतों या उर्वरकों के बारे में पूछ सकते हैं!"
    }
}

def fetch_weather_for_location(query):
    import urllib.request
    import urllib.parse
    import json
    try:
        encoded_query = urllib.parse.quote(query)
        # Try Open-Meteo Geocoding API first
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_query}&count=1&language=en&format=json"
        
        req = urllib.request.Request(geocode_url, headers={'User-Agent': 'HanuAgri/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            geo_data = json.loads(response.read().decode('utf-8'))
            
        if not geo_data.get('results'):
            # Fallback to Nominatim (OpenStreetMap) if city not found
            nom_url = f"https://nominatim.openstreetmap.org/search?q={encoded_query}&format=json&limit=1"
            req_nom = urllib.request.Request(nom_url, headers={'User-Agent': 'HanuAgri/1.0 (Contact: admin@example.com)'})
            with urllib.request.urlopen(req_nom, timeout=5) as response_nom:
                nom_data = json.loads(response_nom.read().decode('utf-8'))
                
            if not nom_data:
                return None
                
            loc = nom_data[0]
            lat = float(loc['lat'])
            lon = float(loc['lon'])
            
            # Make the name cleaner if possible from display_name
            display_parts = loc.get('display_name', query.title()).split(',')
            location_name = f"{display_parts[0]}, {display_parts[-3].strip() if len(display_parts) > 2 else ''}".strip(', ')
        else:
            loc = geo_data['results'][0]
            lat = loc['latitude']
            lon = loc['longitude']
            name = loc['name']
            admin1 = loc.get('admin1', '')
            country = loc.get('country', '')
            
            location_name = f"{name}, {admin1}" if admin1 else name
            if country and country != 'India':
                location_name += f", {country}"
            
            
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,wind_speed_10m&timezone=auto"
        
        req_w = urllib.request.Request(weather_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_w, timeout=5) as response:
            w_data = json.loads(response.read().decode('utf-8'))
            
        current = w_data.get('current', {})
        code = current.get('weather_code', 0)
        
        weather_desc = {
            0: ("Clear sky", "☀️"),
            1: ("Mainly clear", "🌤️"),
            2: ("Partly cloudy", "⛅"),
            3: ("Overcast", "☁️"),
            45: ("Foggy", "🌫️"),
            48: ("Depositing rime fog", "🌫️"),
            51: ("Light drizzle", "🌧️"),
            53: ("Moderate drizzle", "🌧️"),
            55: ("Dense drizzle", "🌧️"),
            56: ("Light freezing drizzle", "🌧️"),
            57: ("Dense freezing drizzle", "🌧️"),
            61: ("Slight rain", "🌧️"),
            63: ("Moderate rain", "🌧️"),
            65: ("Heavy rain", "🌧️"),
            66: ("Light freezing rain", "🌧️"),
            67: ("Heavy freezing rain", "🌧️"),
            71: ("Slight snowfall", "❄️"),
            73: ("Moderate snowfall", "❄️"),
            75: ("Heavy snowfall", "❄️"),
            77: ("Snow grains", "❄️"),
            80: ("Slight rain showers", "🌦️"),
            81: ("Moderate rain showers", "🌦️"),
            82: ("Violent rain showers", "🌦️"),
            85: ("Slight snow showers", "❄️"),
            86: ("Heavy snow showers", "❄️"),
            95: ("Thunderstorm", "⛈️"),
            96: ("Thunderstorm with slight hail", "⛈️"),
            99: ("Thunderstorm with heavy hail", "⛈️"),
        }
        
        desc, emoji = weather_desc.get(code, ("Clear sky", "☀️"))
        
        return {
            'location': location_name,
            'temp': current.get('temperature_2m'),
            'humidity': current.get('relative_humidity_2m'),
            'feels_like': current.get('apparent_temperature'),
            'wind_speed': current.get('wind_speed_10m'),
            'precipitation': current.get('precipitation', 0),
            'description': desc,
            'emoji': emoji
        }
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

def match_commodity(text):
    text_lower = text.lower()
    commodities = ['rice', 'wheat', 'maize', 'cotton', 'sugarcane', 'groundnut', 'soybean', 'onion', 'tomato', 'potato', 'banana', 'mango', 'coconut', 'coffee', 'turmeric']
    for c in commodities:
        if c in text_lower:
            return c.capitalize()
    return None

def match_state(text):
    text_lower = text.lower()
    states = ['karnataka', 'maharashtra', 'tamil nadu', 'andhra pradesh', 'kerala', 'uttar pradesh', 'madhya pradesh', 'gujarat', 'rajasthan', 'punjab']
    for s in states:
        if s in text_lower:
            if s == 'tamil nadu': return 'Tamil Nadu'
            if s == 'andhra pradesh': return 'Andhra Pradesh'
            if s == 'uttar pradesh': return 'Uttar Pradesh'
            if s == 'madhya pradesh': return 'Madhya Pradesh'
            return s.capitalize()
    return None

def clean_weather_query(text):
    text = text.lower()
    import re
    # Replace all punctuation and emojis with spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\b(weather|report|forecast|temperature|temp|climate|how is the|what is the|current|live|in|at|for|show me the|tell me the)\b', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ── API: Chatbot Assistant ───────────────────────────────────────────────────
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json or {}
        message = data.get('message', '').strip()
        lang = data.get('lang', 'en').lower()
        if lang not in CHAT_TRANSLATIONS:
            lang = 'en'
            
        trans = CHAT_TRANSLATIONS[lang]
        
        if not message:
            return jsonify({
                'success': True,
                'type': 'text',
                'text': trans['greet']
            })
            
        msg_lower = message.lower()
        
        # 1. GREETING INTENT
        greetings = ['hi', 'hello', 'hey', 'namaste', 'greetings', 'who are you', 'how are you', 'help', 'start']
        if any(msg_lower == g or msg_lower.startswith(g + ' ') for g in greetings):
            return jsonify({
                'success': True,
                'type': 'text',
                'text': trans['greet']
            })
            
        # 2. WEATHER INTENT
        weather_words = ['weather', 'temperature', 'temp', 'rain', 'climate', 'forecast', 'humidity']
        if any(w in msg_lower for w in weather_words):
            city_query = clean_weather_query(message)
            if not city_query or city_query in weather_words:
                return jsonify({
                    'success': True,
                    'type': 'text',
                    'text': trans['weather_prompt'] + "<br><br><i>Tip: Try asking like 'Weather in Pandavapura'</i>"
                })
            
            weather_data = fetch_weather_for_location(city_query)
            if weather_data:
                return jsonify({
                    'success': True,
                    'type': 'weather',
                    'text': f"Weather in {weather_data['location']}: {weather_data['emoji']} {weather_data['description']}, Temp: {weather_data['temp']}°C, Humidity: {weather_data['humidity']}%",
                    'data': weather_data
                })
            else:
                return jsonify({
                    'success': True,
                    'type': 'text',
                    'text': trans['weather_err'].format(query=city_query.capitalize())
                })
                
        # 3. FERTILIZER PRICE INTENT
        fertilizer_price_words = ['fertilizer price', 'fertiliser price', 'price of fertilizer', 'cost of fertilizer', 'urea price', 'dap price', 'mop price', 'npk price', 'fertilizer cost', 'fertiliser cost']
        if any(w in msg_lower for w in fertilizer_price_words) or (('fertilizer' in msg_lower or 'fertiliser' in msg_lower) and ('price' in msg_lower or 'cost' in msg_lower or 'rate' in msg_lower)):
            return jsonify({
                'success': True,
                'type': 'fertilizer_price',
                'text': "Here are the current subsidized prices of common fertilizers in India.",
                'data': FERTILIZER_PRICES
            })
            
        # 4. FERTILIZER RECOMMENDATION INTENT
        fertilizer_guide_words = ['what fertilizer', 'use fertilizer', 'fertilizer for', 'which fertilizer for', 'plant fertilizer', 'fertilizer recommendation', 'best fertilizer for']
        if any(w in msg_lower for w in fertilizer_guide_words) or (('fertilizer' in msg_lower or 'fertiliser' in msg_lower) and ('crop' in msg_lower or 'plant' in msg_lower or 'use' in msg_lower)):
            crop = match_commodity(message)
            if not crop:
                for key in CROP_FERTILIZER_GUIDE.keys():
                    if key.lower() in msg_lower:
                        crop = key
                        break
            
            if crop:
                guide = CROP_FERTILIZER_GUIDE.get(crop)
                if guide:
                    return jsonify({
                        'success': True,
                        'type': 'fertilizer_guide',
                        'text': f"Recommended fertilizer for {crop}: {guide['fertilizer']}. {guide['why']}",
                        'data': {
                            'crop': crop,
                            'fertilizer': guide['fertilizer'],
                            'why': guide['why'],
                            'usage': guide['usage'],
                            'tips': guide['tips']
                        }
                    })
            
            return jsonify({
                'success': True,
                'type': 'text',
                'text': trans['fert_guide_prompt']
            })
            
        # 5. CROP PRICE INTENT
        crop_price_words = ['crop price', 'commodity price', 'price of', 'price of crop', 'market price', 'modal price', 'rate of', 'cost of rice', 'cost of wheat', 'how much is']
        is_price_query = any(w in msg_lower for w in crop_price_words) or ('price' in msg_lower or 'rate' in msg_lower)
        commodity = match_commodity(message)
        
        if commodity or is_price_query:
            if not commodity:
                return jsonify({
                    'success': True,
                    'type': 'text',
                    'text': trans['crop_price_prompt']
                })
                
            state = match_state(message) or 'Karnataka'
            
            result = price_predictor.predict_future(commodity, state, days=1)
            
            if 'error' in result:
                return jsonify({
                    'success': True,
                    'type': 'text',
                    'text': trans['crop_price_err'].format(commodity=commodity, state=state)
                })
                
            prediction = result['predictions'][0]
            
            return jsonify({
                'success': True,
                'type': 'crop_price',
                'text': f"The current predicted market price of {commodity} in {state} is ₹{prediction['predicted_price']}/quintal (Range: ₹{prediction['min_price']} - ₹{prediction['max_price']}).",
                'data': {
                    'commodity': commodity,
                    'state': state,
                    'date': prediction['date'],
                    'predicted_price': prediction['predicted_price'],
                    'min_price': prediction['min_price'],
                    'max_price': prediction['max_price'],
                    'trend': result.get('summary', {}).get('trend', 'stable')
                }
            })
            
        return jsonify({
            'success': True,
            'type': 'default',
            'text': trans['default']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # Generate datasets if they don't exist
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    if not os.path.exists(os.path.join(data_dir, 'crop_data.csv')):
        print("📊 Generating datasets for the first time...")
        import subprocess
        subprocess.run([sys.executable, os.path.join(data_dir, 'generate_datasets.py')])
    
    # Train models if not already trained
    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
    if not os.path.exists(os.path.join(models_dir, 'crop_model.pkl')):
        print("🧠 Training ML models for the first time...")
        crop_recommender.train()
        fertilizer_recommender.train()
        price_predictor.train()
        print("✅ All models trained!")
    else:
        crop_recommender.load()
        fertilizer_recommender.load()
        price_predictor.load()
        print("✅ Pre-trained models loaded!")
    
    print("\n🚀 Starting Agricultural AI Server on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
