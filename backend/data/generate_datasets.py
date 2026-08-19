"""
Generate synthetic datasets for the Agricultural Demand Prediction system.
Produces CSV files for crop recommendation, fertilizer recommendation,
and commodity price prediction training.
"""
import csv
import random
import os
import json
from datetime import datetime, timedelta

random.seed(42)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Crop Recommendation Dataset ──────────────────────────────────────────────
CROPS = {
    'Rice':       {'N': (60, 100), 'P': (35, 65), 'K': (35, 55), 'temp': (20, 28), 'humidity': (75, 95), 'ph': (5.5, 7.0), 'rainfall': (180, 300)},
    'Wheat':      {'N': (80, 130), 'P': (40, 70), 'K': (15, 40), 'temp': (12, 24), 'humidity': (50, 75), 'ph': (6.0, 7.5), 'rainfall': (50, 120)},
    'Maize':      {'N': (60, 100), 'P': (35, 65), 'K': (25, 50), 'temp': (18, 30), 'humidity': (55, 80), 'ph': (5.5, 7.5), 'rainfall': (60, 120)},
    'Cotton':     {'N': (100, 150), 'P': (40, 70), 'K': (15, 35), 'temp': (22, 35), 'humidity': (45, 70), 'ph': (6.0, 8.0), 'rainfall': (50, 100)},
    'Sugarcane':  {'N': (80, 130), 'P': (20, 50), 'K': (20, 50), 'temp': (22, 35), 'humidity': (70, 95), 'ph': (5.5, 7.5), 'rainfall': (150, 250)},
    'Jute':       {'N': (60, 100), 'P': (35, 60), 'K': (35, 55), 'temp': (24, 37), 'humidity': (70, 95), 'ph': (5.5, 7.0), 'rainfall': (150, 250)},
    'Coffee':     {'N': (90, 130), 'P': (15, 40), 'K': (25, 45), 'temp': (15, 28), 'humidity': (55, 85), 'ph': (5.5, 7.0), 'rainfall': (120, 200)},
    'Coconut':    {'N': (15, 35), 'P': (5, 25),  'K': (25, 50), 'temp': (25, 35), 'humidity': (70, 95), 'ph': (5.0, 7.0), 'rainfall': (120, 250)},
    'Groundnut':  {'N': (10, 30), 'P': (35, 65), 'K': (60, 85), 'temp': (25, 33), 'humidity': (55, 80), 'ph': (5.5, 7.5), 'rainfall': (50, 100)},
    'Banana':     {'N': (80, 130), 'P': (50, 80), 'K': (45, 75), 'temp': (25, 35), 'humidity': (70, 95), 'ph': (5.5, 7.0), 'rainfall': (80, 150)},
    'Mango':      {'N': (15, 40), 'P': (15, 45), 'K': (25, 55), 'temp': (24, 36), 'humidity': (50, 80), 'ph': (5.5, 7.5), 'rainfall': (60, 150)},
    'Grapes':     {'N': (15, 35), 'P': (100, 150), 'K': (180, 220), 'temp': (8, 36), 'humidity': (70, 90), 'ph': (5.5, 7.0), 'rainfall': (60, 100)},
    'Apple':      {'N': (15, 35), 'P': (120, 150), 'K': (190, 220), 'temp': (8, 24), 'humidity': (80, 95), 'ph': (5.5, 7.0), 'rainfall': (100, 160)},
    'Orange':     {'N': (15, 30), 'P': (5, 20),  'K': (5, 20),  'temp': (10, 35), 'humidity': (80, 95), 'ph': (6.0, 8.0), 'rainfall': (90, 130)},
    'Papaya':     {'N': (40, 70), 'P': (55, 80), 'K': (45, 65), 'temp': (25, 38), 'humidity': (80, 95), 'ph': (6.0, 7.5), 'rainfall': (120, 180)},
    'Pomegranate':{'N': (5, 20),  'P': (5, 20),  'K': (35, 55), 'temp': (18, 36), 'humidity': (80, 95), 'ph': (5.5, 7.5), 'rainfall': (30, 70)},
    'Lentil':     {'N': (10, 30), 'P': (55, 85), 'K': (15, 30), 'temp': (18, 30), 'humidity': (30, 60), 'ph': (6.0, 8.0), 'rainfall': (30, 60)},
    'Chickpea':   {'N': (30, 60), 'P': (55, 85), 'K': (70, 95), 'temp': (15, 30), 'humidity': (15, 50), 'ph': (6.0, 8.0), 'rainfall': (50, 100)},
    'Pigeonpeas': {'N': (15, 35), 'P': (55, 85), 'K': (15, 35), 'temp': (18, 36), 'humidity': (30, 65), 'ph': (5.5, 7.5), 'rainfall': (120, 180)},
    'Mothbeans':  {'N': (15, 35), 'P': (40, 65), 'K': (15, 30), 'temp': (24, 32), 'humidity': (40, 65), 'ph': (3.5, 5.5), 'rainfall': (30, 70)},
    'Mungbean':   {'N': (15, 35), 'P': (40, 65), 'K': (15, 30), 'temp': (25, 35), 'humidity': (80, 95), 'ph': (6.0, 7.5), 'rainfall': (30, 60)},
    'Blackgram':  {'N': (30, 50), 'P': (55, 80), 'K': (15, 30), 'temp': (25, 35), 'humidity': (55, 80), 'ph': (6.0, 8.0), 'rainfall': (55, 80)},
}

def generate_crop_data(n_per_crop=100):
    rows = []
    for crop, params in CROPS.items():
        for _ in range(n_per_crop):
            row = {
                'N': round(random.uniform(*params['N']), 1),
                'P': round(random.uniform(*params['P']), 1),
                'K': round(random.uniform(*params['K']), 1),
                'temperature': round(random.uniform(*params['temp']), 2),
                'humidity': round(random.uniform(*params['humidity']), 2),
                'ph': round(random.uniform(*params['ph']), 2),
                'rainfall': round(random.uniform(*params['rainfall']), 2),
                'label': crop
            }
            rows.append(row)
    random.shuffle(rows)
    path = os.path.join(DATA_DIR, 'crop_data.csv')
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])
        writer.writeheader()
        writer.writerows(rows)
    print(f"✓ Generated {len(rows)} crop samples → {path}")


# ── Fertilizer Recommendation Dataset ────────────────────────────────────────
FERTILIZER_MAP = {
    ('Low', 'Low',  'Low'):  'NPK 20-20-20',
    ('Low', 'Low',  'Normal'): 'DAP (Diammonium Phosphate)',
    ('Low', 'Low',  'High'): 'DAP (Diammonium Phosphate)',
    ('Low', 'Normal','Low'):  'MOP (Muriate of Potash)',
    ('Low', 'Normal','Normal'): 'Urea',
    ('Low', 'Normal','High'): 'Urea',
    ('Low', 'High', 'Low'):  'MOP (Muriate of Potash)',
    ('Low', 'High', 'Normal'): 'Urea',
    ('Low', 'High', 'High'): 'Urea',
    ('Normal','Low', 'Low'):  'SSP (Single Super Phosphate)',
    ('Normal','Low', 'Normal'): 'SSP (Single Super Phosphate)',
    ('Normal','Low', 'High'): 'SSP (Single Super Phosphate)',
    ('Normal','Normal','Low'): 'MOP (Muriate of Potash)',
    ('Normal','Normal','Normal'): 'Balanced NPK 10-10-10',
    ('Normal','Normal','High'): 'Balanced NPK 10-10-10',
    ('Normal','High','Low'):  'MOP (Muriate of Potash)',
    ('Normal','High','Normal'): 'Balanced NPK 10-10-10',
    ('Normal','High','High'): 'No Fertilizer Needed',
    ('High', 'Low', 'Low'):  'SSP (Single Super Phosphate)',
    ('High', 'Low', 'Normal'): 'SSP (Single Super Phosphate)',
    ('High', 'Low', 'High'): 'SSP (Single Super Phosphate)',
    ('High', 'Normal','Low'): 'MOP (Muriate of Potash)',
    ('High', 'Normal','Normal'): 'No Fertilizer Needed',
    ('High', 'Normal','High'): 'No Fertilizer Needed',
    ('High', 'High', 'Low'):  'MOP (Muriate of Potash)',
    ('High', 'High', 'Normal'): 'No Fertilizer Needed',
    ('High', 'High', 'High'): 'No Fertilizer Needed',
}

SOIL_TYPES = ['Sandy', 'Loamy', 'Black', 'Red', 'Clayey']
CROP_LIST = list(CROPS.keys())

def classify_level(value, low_thresh, high_thresh):
    if value < low_thresh:
        return 'Low'
    elif value > high_thresh:
        return 'High'
    return 'Normal'

def generate_fertilizer_data(n=2000):
    rows = []
    for _ in range(n):
        n_val = round(random.uniform(0, 150), 1)
        p_val = round(random.uniform(0, 150), 1)
        k_val = round(random.uniform(0, 220), 1)
        temp  = round(random.uniform(10, 45), 1)
        hum   = round(random.uniform(20, 100), 1)
        moist = round(random.uniform(10, 90), 1)
        soil  = random.choice(SOIL_TYPES)
        crop  = random.choice(CROP_LIST)

        n_level = classify_level(n_val, 40, 100)
        p_level = classify_level(p_val, 40, 80)
        k_level = classify_level(k_val, 30, 80)

        fertilizer = FERTILIZER_MAP.get((n_level, p_level, k_level), 'Balanced NPK 10-10-10')

        rows.append({
            'temperature': temp, 'humidity': hum, 'moisture': moist,
            'soil_type': soil, 'crop_type': crop,
            'nitrogen': n_val, 'phosphorous': p_val, 'potassium': k_val,
            'fertilizer': fertilizer
        })
    random.shuffle(rows)
    path = os.path.join(DATA_DIR, 'fertilizer_data.csv')
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'temperature', 'humidity', 'moisture', 'soil_type', 'crop_type',
            'nitrogen', 'phosphorous', 'potassium', 'fertilizer'
        ])
        writer.writeheader()
        writer.writerows(rows)
    print(f"✓ Generated {len(rows)} fertilizer samples → {path}")


# ── Commodity Price Dataset ──────────────────────────────────────────────────
COMMODITIES = {
    'Rice':      {'base': 2200, 'volatility': 200, 'trend': 50},
    'Wheat':     {'base': 2400, 'volatility': 250, 'trend': 40},
    'Maize':     {'base': 1800, 'volatility': 300, 'trend': 30},
    'Cotton':    {'base': 6000, 'volatility': 800, 'trend': 100},
    'Sugarcane': {'base': 350,  'volatility': 50,  'trend': 10},
    'Groundnut': {'base': 5500, 'volatility': 600, 'trend': 80},
    'Soybean':   {'base': 4200, 'volatility': 500, 'trend': 60},
    'Onion':     {'base': 1500, 'volatility': 800, 'trend': 20},
    'Tomato':    {'base': 1200, 'volatility': 1000,'trend': 10},
    'Potato':    {'base': 1000, 'volatility': 400, 'trend': 15},
    'Banana':    {'base': 2000, 'volatility': 300, 'trend': 25},
    'Mango':     {'base': 3500, 'volatility': 1000,'trend': 50},
    'Coconut':   {'base': 2500, 'volatility': 400, 'trend': 35},
    'Coffee':    {'base': 8000, 'volatility': 1500,'trend': 120},
    'Turmeric':  {'base': 7000, 'volatility': 1200,'trend': 90},
}

STATES = ['Karnataka', 'Maharashtra', 'Tamil Nadu', 'Andhra Pradesh', 'Kerala',
          'Uttar Pradesh', 'Madhya Pradesh', 'Gujarat', 'Rajasthan', 'Punjab']

MARKETS = {
    'Karnataka': ['Bangalore', 'Mysore', 'Hubli', 'Mandya', 'Shimoga'],
    'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad'],
    'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Salem', 'Trichy'],
    'Andhra Pradesh': ['Hyderabad', 'Vijayawada', 'Visakhapatnam', 'Tirupati', 'Guntur'],
    'Kerala': ['Kochi', 'Thiruvananthapuram', 'Kozhikode', 'Thrissur', 'Kollam'],
    'Uttar Pradesh': ['Lucknow', 'Agra', 'Varanasi', 'Kanpur', 'Allahabad'],
    'Madhya Pradesh': ['Bhopal', 'Indore', 'Jabalpur', 'Gwalior', 'Ujjain'],
    'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar'],
    'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota', 'Ajmer'],
    'Punjab': ['Ludhiana', 'Amritsar', 'Jalandhar', 'Patiala', 'Bathinda'],
}

def generate_price_data():
    rows = []
    start_date = datetime(2019, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    for commodity, params in COMMODITIES.items():
        for state in STATES:
            markets = MARKETS[state]
            market = random.choice(markets)
            current_date = start_date
            prev_price = params['base']
            
            while current_date <= end_date:
                # Seasonal factor (sinusoidal)
                day_of_year = current_date.timetuple().tm_yday
                seasonal = params['volatility'] * 0.5 * \
                    (0.7 * __import__('math').sin(2 * 3.14159 * day_of_year / 365) +
                     0.3 * __import__('math').cos(4 * 3.14159 * day_of_year / 365))
                
                # Trend factor (gradual yearly increase)
                years_elapsed = (current_date - start_date).days / 365.25
                trend = params['trend'] * years_elapsed
                
                # Random daily fluctuation
                noise = random.gauss(0, params['volatility'] * 0.1)
                
                # Price with momentum
                price = params['base'] + seasonal + trend + noise
                price = max(price * 0.5, price)  # floor at 50% of base
                price = 0.7 * price + 0.3 * prev_price  # smoothing
                prev_price = price
                
                # Generate min/max around modal price
                modal_price = round(price, 2)
                min_price = round(modal_price * random.uniform(0.85, 0.95), 2)
                max_price = round(modal_price * random.uniform(1.05, 1.15), 2)
                
                rows.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'state': state,
                    'market': market,
                    'commodity': commodity,
                    'min_price': min_price,
                    'max_price': max_price,
                    'modal_price': modal_price,
                })
                
                # Skip some days randomly for realism
                current_date += timedelta(days=random.choice([1, 1, 1, 2, 3]))
    
    random.shuffle(rows)
    path = os.path.join(DATA_DIR, 'price_data.csv')
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'date', 'state', 'market', 'commodity',
            'min_price', 'max_price', 'modal_price'
        ])
        writer.writeheader()
        writer.writerows(rows)
    print(f"✓ Generated {len(rows)} price records → {path}")


# ── Disease Detection Labels ─────────────────────────────────────────────────
DISEASES = {
    "Healthy": {
        "description": "The plant leaf appears healthy with no visible signs of disease.",
        "treatment": "Continue regular maintenance. Ensure proper watering, sunlight, and nutrient supply."
    },
    "Bacterial Blight": {
        "description": "Water-soaked lesions on leaves that turn brown and dry. Common in rice and cotton.",
        "treatment": "Remove infected plant parts. Apply copper-based bactericides. Use resistant varieties. Avoid overhead irrigation."
    },
    "Leaf Rust": {
        "description": "Orange-brown pustules on the underside of leaves. Common in wheat and barley.",
        "treatment": "Apply fungicides like Propiconazole or Tebuconazole. Use rust-resistant crop varieties. Ensure proper spacing."
    },
    "Powdery Mildew": {
        "description": "White powdery coating on leaves and stems. Common in grapes, wheat, and vegetables.",
        "treatment": "Apply sulfur-based or systemic fungicides. Improve air circulation. Remove infected leaves. Avoid overhead watering."
    },
    "Late Blight": {
        "description": "Dark, water-soaked patches on leaves that spread rapidly. Major disease of potato and tomato.",
        "treatment": "Apply Mancozeb or Metalaxyl-based fungicides. Remove infected plants immediately. Ensure good drainage. Use certified disease-free seeds."
    },
    "Leaf Spot": {
        "description": "Circular brown or black spots on leaves with yellow halos. Common in many crops.",
        "treatment": "Apply Carbendazim or Chlorothalonil. Remove and destroy infected leaves. Practice crop rotation. Maintain field hygiene."
    },
    "Yellow Mosaic Virus": {
        "description": "Yellow and green mosaic patterns on leaves, causing stunted growth. Common in legumes.",
        "treatment": "Control whitefly vectors using Imidacloprid. Remove infected plants. Use virus-resistant varieties. Apply neem oil as a preventive."
    },
    "Anthracnose": {
        "description": "Dark, sunken lesions on leaves, stems, and fruits. Common in mango, chili, and beans.",
        "treatment": "Apply Mancozeb or Copper Oxychloride sprays. Prune infected branches. Avoid working in wet fields. Use disease-free seeds."
    },
    "Downy Mildew": {
        "description": "Yellow patches on upper leaf surface with fuzzy growth underneath. Common in grapes and cucurbits.",
        "treatment": "Apply Metalaxyl or Ridomil MZ. Ensure good air circulation. Remove infected leaves. Avoid excess moisture."
    },
    "Fusarium Wilt": {
        "description": "Yellowing and wilting of leaves, starting from lower parts. Vascular browning visible on cutting stem.",
        "treatment": "Soil treatment with Trichoderma viride. Use resistant varieties. Practice long crop rotation (3-4 years). Maintain proper soil pH."
    }
}

def generate_disease_data():
    path = os.path.join(DATA_DIR, 'disease_labels.json')
    with open(path, 'w') as f:
        json.dump(DISEASES, f, indent=2)
    print(f"✓ Generated {len(DISEASES)} disease labels → {path}")


# ── Government Schemes ───────────────────────────────────────────────────────
SCHEMES = [
    {
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "description": "Direct income support of ₹6,000 per year to small and marginal farmer families, paid in three equal installments.",
        "eligibility": "All land-holding farmer families with cultivable land up to 2 hectares.",
        "benefit": "₹6,000 per year (₹2,000 every 4 months)",
        "link": "https://pmkisan.gov.in",
        "category": "Income Support"
    },
    {
        "name": "PM Fasal Bima Yojana (PMFBY)",
        "description": "Crop insurance scheme providing financial support to farmers suffering crop loss due to natural calamities, pests, and diseases.",
        "eligibility": "All farmers growing notified crops in notified areas. Both loanee and non-loanee farmers can apply.",
        "benefit": "Subsidised premium: 2% for Kharif, 1.5% for Rabi, 5% for commercial crops",
        "link": "https://pmfby.gov.in",
        "category": "Crop Insurance"
    },
    {
        "name": "Kisan Credit Card (KCC)",
        "description": "Provides affordable credit to farmers for crop production, post-harvest expenses, and consumption needs.",
        "eligibility": "All farmers, including tenant farmers, sharecroppers, and self-help groups.",
        "benefit": "Credit up to ₹3 lakh at 4% interest rate (with prompt repayment subvention)",
        "link": "https://www.pmkisan.gov.in/KCC.aspx",
        "category": "Credit"
    },
    {
        "name": "Soil Health Card Scheme",
        "description": "Government provides soil health cards to farmers carrying crop-wise recommendations for nutrients and fertilizers.",
        "eligibility": "All farmers across India.",
        "benefit": "Free soil testing and customized fertilizer recommendations every 2 years",
        "link": "https://soilhealth.dac.gov.in",
        "category": "Soil Health"
    },
    {
        "name": "e-NAM (National Agriculture Market)",
        "description": "Pan-India electronic trading portal networking existing APMC mandis to create a unified national market for agricultural commodities.",
        "eligibility": "Farmers, traders, and buyers registered at APMC mandis.",
        "benefit": "Better price discovery, transparent bidding, reduced intermediaries",
        "link": "https://enam.gov.in",
        "category": "Market Access"
    },
    {
        "name": "Paramparagat Krishi Vikas Yojana (PKVY)",
        "description": "Promotes organic farming through cluster approach. Supports farmers in adopting organic practices.",
        "eligibility": "Groups of 50+ farmers in a cluster of 20 hectares.",
        "benefit": "₹50,000 per hectare over 3 years for organic inputs and certification",
        "link": "https://pgsindia-ncof.gov.in",
        "category": "Organic Farming"
    },
    {
        "name": "Rashtriya Krishi Vikas Yojana (RKVY)",
        "description": "Incentivizes states to increase public investment in agriculture by providing flexible funding.",
        "eligibility": "State-level implementation; benefits reach all farmer categories.",
        "benefit": "Infrastructure development, technology adoption, and capacity building",
        "link": "https://rkvy.nic.in",
        "category": "Development"
    },
    {
        "name": "PM Krishi Sinchayee Yojana (PMKSY)",
        "description": "Ensures access to protective irrigation through 'Har Khet Ko Pani' and promotes micro-irrigation.",
        "eligibility": "All farmers, with priority to small and marginal farmers.",
        "benefit": "Subsidy up to 55% for sprinkler and 45% for drip irrigation (higher for SC/ST)",
        "link": "https://pmksy.gov.in",
        "category": "Irrigation"
    },
]

def generate_schemes_data():
    path = os.path.join(DATA_DIR, 'government_schemes.json')
    with open(path, 'w') as f:
        json.dump(SCHEMES, f, indent=2)
    print(f"✓ Generated {len(SCHEMES)} government schemes → {path}")


if __name__ == '__main__':
    print("🌾 Generating Agricultural Datasets...\n")
    generate_crop_data()
    generate_fertilizer_data()
    generate_price_data()
    generate_disease_data()
    generate_schemes_data()
    print("\n✅ All datasets generated successfully!")
