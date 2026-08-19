"""
Crop Profitability & ROI Calculator
Calculates land-size based financial investment, cost of cultivation,
projected revenue, net profit, and ROI % for farmers.
"""

class ProfitabilityCalculator:
    def __init__(self):
        # Base benchmarks per acre (in INR) and average yield (in quintals/acre)
        self.crop_benchmarks = {
            'Rice': {'seed_cost': 1800, 'land_prep': 3500, 'fertilizer_pesticide': 4200, 'labor': 8500, 'irrigation': 3000, 'harvest_transport': 4000, 'yield_per_acre_qtl': 22, 'avg_price_per_qtl': 2600},
            'Wheat': {'seed_cost': 2000, 'land_prep': 3000, 'fertilizer_pesticide': 3800, 'labor': 6500, 'irrigation': 2500, 'harvest_transport': 3500, 'yield_per_acre_qtl': 19, 'avg_price_per_qtl': 2450},
            'Maize': {'seed_cost': 2500, 'land_prep': 2800, 'fertilizer_pesticide': 3200, 'labor': 5500, 'irrigation': 2000, 'harvest_transport': 3000, 'yield_per_acre_qtl': 24, 'avg_price_per_qtl': 2100},
            'Cotton': {'seed_cost': 3500, 'land_prep': 3800, 'fertilizer_pesticide': 6500, 'labor': 9500, 'irrigation': 3500, 'harvest_transport': 4200, 'yield_per_acre_qtl': 12, 'avg_price_per_qtl': 6800},
            'Sugarcane': {'seed_cost': 7000, 'land_prep': 6000, 'fertilizer_pesticide': 8500, 'labor': 14000, 'irrigation': 6000, 'harvest_transport': 7500, 'yield_per_acre_qtl': 350, 'avg_price_per_qtl': 340},
            'Chickpea': {'seed_cost': 1600, 'land_prep': 2200, 'fertilizer_pesticide': 2500, 'labor': 4500, 'irrigation': 1500, 'harvest_transport': 2200, 'yield_per_acre_qtl': 9, 'avg_price_per_qtl': 5600},
            'Kidney Beans': {'seed_cost': 2200, 'land_prep': 2500, 'fertilizer_pesticide': 2800, 'labor': 5000, 'irrigation': 1800, 'harvest_transport': 2500, 'yield_per_acre_qtl': 8, 'avg_price_per_qtl': 7200},
            'Pigeon Peas': {'seed_cost': 1500, 'land_prep': 2300, 'fertilizer_pesticide': 2700, 'labor': 4800, 'irrigation': 1600, 'harvest_transport': 2400, 'yield_per_acre_qtl': 7, 'avg_price_per_qtl': 6900},
            'Moth Beans': {'seed_cost': 1200, 'land_prep': 1800, 'fertilizer_pesticide': 1900, 'labor': 3800, 'irrigation': 1200, 'harvest_transport': 1800, 'yield_per_acre_qtl': 6, 'avg_price_per_qtl': 6100},
            'Mung Bean': {'seed_cost': 1400, 'land_prep': 2000, 'fertilizer_pesticide': 2200, 'labor': 4200, 'irrigation': 1400, 'harvest_transport': 2000, 'yield_per_acre_qtl': 6, 'avg_price_per_qtl': 7400},
            'Black Gram': {'seed_cost': 1500, 'land_prep': 2100, 'fertilizer_pesticide': 2300, 'labor': 4300, 'irrigation': 1500, 'harvest_transport': 2100, 'yield_per_acre_qtl': 6, 'avg_price_per_qtl': 7100},
            'Lentil': {'seed_cost': 1600, 'land_prep': 2200, 'fertilizer_pesticide': 2400, 'labor': 4400, 'irrigation': 1500, 'harvest_transport': 2200, 'yield_per_acre_qtl': 7, 'avg_price_per_qtl': 6300},
            'Pomegranate': {'seed_cost': 12000, 'land_prep': 8000, 'fertilizer_pesticide': 14000, 'labor': 16000, 'irrigation': 7000, 'harvest_transport': 8000, 'yield_per_acre_qtl': 50, 'avg_price_per_qtl': 6500},
            'Banana': {'seed_cost': 9000, 'land_prep': 6000, 'fertilizer_pesticide': 11000, 'labor': 15000, 'irrigation': 6500, 'harvest_transport': 7000, 'yield_per_acre_qtl': 220, 'avg_price_per_qtl': 1800},
            'Mango': {'seed_cost': 8000, 'land_prep': 5000, 'fertilizer_pesticide': 9000, 'labor': 12000, 'irrigation': 5000, 'harvest_transport': 6000, 'yield_per_acre_qtl': 45, 'avg_price_per_qtl': 4200},
            'Grapes': {'seed_cost': 15000, 'land_prep': 10000, 'fertilizer_pesticide': 18000, 'labor': 22000, 'irrigation': 8000, 'harvest_transport': 9000, 'yield_per_acre_qtl': 80, 'avg_price_per_qtl': 5800},
            'Watermelon': {'seed_cost': 3500, 'land_prep': 3000, 'fertilizer_pesticide': 4500, 'labor': 6500, 'irrigation': 3000, 'harvest_transport': 3500, 'yield_per_acre_qtl': 150, 'avg_price_per_qtl': 950},
            'Muskmelon': {'seed_cost': 3200, 'land_prep': 2800, 'fertilizer_pesticide': 4200, 'labor': 6000, 'irrigation': 2800, 'harvest_transport': 3200, 'yield_per_acre_qtl': 120, 'avg_price_per_qtl': 1400},
            'Apple': {'seed_cost': 14000, 'land_prep': 9000, 'fertilizer_pesticide': 16000, 'labor': 18000, 'irrigation': 7000, 'harvest_transport': 8500, 'yield_per_acre_qtl': 70, 'avg_price_per_qtl': 7500},
            'Orange': {'seed_cost': 9500, 'land_prep': 6000, 'fertilizer_pesticide': 10000, 'labor': 13000, 'irrigation': 5500, 'harvest_transport': 6500, 'yield_per_acre_qtl': 60, 'avg_price_per_qtl': 3800},
            'Papaya': {'seed_cost': 4500, 'land_prep': 3500, 'fertilizer_pesticide': 6000, 'labor': 8500, 'irrigation': 4000, 'harvest_transport': 4500, 'yield_per_acre_qtl': 180, 'avg_price_per_qtl': 1250},
            'Coconut': {'seed_cost': 6000, 'land_prep': 4000, 'fertilizer_pesticide': 5500, 'labor': 9000, 'irrigation': 4500, 'harvest_transport': 4000, 'yield_per_acre_qtl': 40, 'avg_price_per_qtl': 3200},
            'Jute': {'seed_cost': 1800, 'land_prep': 2500, 'fertilizer_pesticide': 2800, 'labor': 6000, 'irrigation': 2000, 'harvest_transport': 2800, 'yield_per_acre_qtl': 14, 'avg_price_per_qtl': 4800},
            'Coffee': {'seed_cost': 11000, 'land_prep': 7000, 'fertilizer_pesticide': 12000, 'labor': 16000, 'irrigation': 6000, 'harvest_transport': 7000, 'yield_per_acre_qtl': 10, 'avg_price_per_qtl': 18500}
        }

    def calculate(self, crop, acres=1.0, price_per_qtl=None):
        crop = crop.title() if crop else 'Rice'
        acres = max(0.25, float(acres))
        
        bench = self.crop_benchmarks.get(crop, {
            'seed_cost': 2000, 'land_prep': 3000, 'fertilizer_pesticide': 4000,
            'labor': 7000, 'irrigation': 3000, 'harvest_transport': 3500,
            'yield_per_acre_qtl': 18, 'avg_price_per_qtl': 2500
        })
        
        price = float(price_per_qtl) if price_per_qtl else bench['avg_price_per_qtl']
        
        # Per acre cost breakdown
        seed = int(bench['seed_cost'] * acres)
        land_prep = int(bench['land_prep'] * acres)
        fert_pest = int(bench['fertilizer_pesticide'] * acres)
        labor = int(bench['labor'] * acres)
        irrigation = int(bench['irrigation'] * acres)
        harvest_transport = int(bench['harvest_transport'] * acres)
        
        total_cost = seed + land_prep + fert_pest + labor + irrigation + harvest_transport
        total_yield_qtl = round(bench['yield_per_acre_qtl'] * acres, 1)
        gross_revenue = int(total_yield_qtl * price)
        net_profit = gross_revenue - total_cost
        roi_pct = round((net_profit / max(total_cost, 1)) * 100, 1)
        
        # Calculate matrix comparison for 3 top alternative crops
        comparison = []
        alt_crops = ['Rice', 'Maize', 'Wheat', 'Chickpea', 'Cotton', 'Sugarcane']
        for alt in alt_crops:
            if alt != crop:
                b_alt = self.crop_benchmarks[alt]
                alt_cost = int((b_alt['seed_cost'] + b_alt['land_prep'] + b_alt['fertilizer_pesticide'] + b_alt['labor'] + b_alt['irrigation'] + b_alt['harvest_transport']) * acres)
                alt_yield = b_alt['yield_per_acre_qtl'] * acres
                alt_rev = int(alt_yield * b_alt['avg_price_per_qtl'])
                alt_profit = alt_rev - alt_cost
                alt_roi = round((alt_profit / max(alt_cost, 1)) * 100, 1)
                comparison.append({
                    'crop': alt,
                    'total_cost': alt_cost,
                    'gross_revenue': alt_rev,
                    'net_profit': alt_profit,
                    'roi_pct': alt_roi
                })
        
        # Sort top 3 by ROI
        comparison = sorted(comparison, key=lambda x: x['roi_pct'], reverse=True)[:3]
        
        return {
            'crop': crop,
            'acres': acres,
            'price_per_qtl': price,
            'total_yield_qtl': total_yield_qtl,
            'gross_revenue': gross_revenue,
            'total_cost': total_cost,
            'net_profit': net_profit,
            'roi_pct': roi_pct,
            'cost_breakdown': {
                'Seeds & Planting': seed,
                'Land Prep & Tillage': land_prep,
                'Fertilizer & Pesticide': fert_pest,
                'Labor & Operations': labor,
                'Irrigation & Power': irrigation,
                'Harvest & Transport': harvest_transport
            },
            'comparison_matrix': comparison
        }
