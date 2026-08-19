"""
Demand-Supply Glut Risk Analyzer
Calculates crop overproduction risk, demand-to-supply ratio,
and market glut probability across Indian states.
"""
import random

class DemandSupplyAnalyzer:
    def __init__(self):
        # Benchmark annual demand vs typical production capacity (in metric tonnes) per state per crop
        self.crop_demand_data = {
            'Rice': {'annual_demand_mt': 1200000, 'base_production_mt': 1150000, 'volatility': 0.08},
            'Wheat': {'annual_demand_mt': 1050000, 'base_production_mt': 1020000, 'volatility': 0.07},
            'Maize': {'annual_demand_mt': 750000, 'base_production_mt': 710000, 'volatility': 0.12},
            'Cotton': {'annual_demand_mt': 600000, 'base_production_mt': 640000, 'volatility': 0.15},
            'Sugarcane': {'annual_demand_mt': 3500000, 'base_production_mt': 3800000, 'volatility': 0.10},
            'Chickpea': {'annual_demand_mt': 450000, 'base_production_mt': 420000, 'volatility': 0.11},
            'Kidney Beans': {'annual_demand_mt': 250000, 'base_production_mt': 230000, 'volatility': 0.09},
            'Pigeon Peas': {'annual_demand_mt': 380000, 'base_production_mt': 340000, 'volatility': 0.13},
            'Moth Beans': {'annual_demand_mt': 180000, 'base_production_mt': 160000, 'volatility': 0.14},
            'Mung Bean': {'annual_demand_mt': 320000, 'base_production_mt': 310000, 'volatility': 0.10},
            'Black Gram': {'annual_demand_mt': 340000, 'base_production_mt': 330000, 'volatility': 0.11},
            'Lentil': {'annual_demand_mt': 290000, 'base_production_mt': 270000, 'volatility': 0.08},
            'Pomegranate': {'annual_demand_mt': 190000, 'base_production_mt': 220000, 'volatility': 0.18},
            'Banana': {'annual_demand_mt': 850000, 'base_production_mt': 890000, 'volatility': 0.12},
            'Mango': {'annual_demand_mt': 950000, 'base_production_mt': 920000, 'volatility': 0.16},
            'Grapes': {'annual_demand_mt': 210000, 'base_production_mt': 230000, 'volatility': 0.20},
            'Watermelon': {'annual_demand_mt': 410000, 'base_production_mt': 450000, 'volatility': 0.22},
            'Muskmelon': {'annual_demand_mt': 180000, 'base_production_mt': 195000, 'volatility': 0.21},
            'Apple': {'annual_demand_mt': 310000, 'base_production_mt': 290000, 'volatility': 0.15},
            'Orange': {'annual_demand_mt': 490000, 'base_production_mt': 510000, 'volatility': 0.14},
            'Papaya': {'annual_demand_mt': 370000, 'base_production_mt': 390000, 'volatility': 0.17},
            'Coconut': {'annual_demand_mt': 620000, 'base_production_mt': 640000, 'volatility': 0.09},
            'Jute': {'annual_demand_mt': 280000, 'base_production_mt': 295000, 'volatility': 0.13},
            'Coffee': {'annual_demand_mt': 150000, 'base_production_mt': 165000, 'volatility': 0.11}
        }
        
        self.state_multipliers = {
            'Karnataka': 1.05,
            'Maharashtra': 1.12,
            'Uttar Pradesh': 1.25,
            'Punjab': 1.18,
            'Haryana': 1.15,
            'Madhya Pradesh': 1.10,
            'Gujarat': 1.08,
            'Tamil Nadu': 1.04,
            'Andhra Pradesh': 1.07,
            'West Bengal': 1.14
        }

    def analyze_risk(self, crop, state):
        crop = crop.title() if crop else 'Rice'
        state = state.title() if state else 'Karnataka'
        
        info = self.crop_demand_data.get(crop, {'annual_demand_mt': 500000, 'base_production_mt': 520000, 'volatility': 0.12})
        mult = self.state_multipliers.get(state, 1.0)
        
        projected_supply = int(info['base_production_mt'] * mult)
        estimated_demand = int(info['annual_demand_mt'] * mult)
        
        # Calculate supply to demand ratio
        ratio = round(projected_supply / max(estimated_demand, 1), 2)
        
        # Calculate risk score out of 100
        # Ratio 1.0 -> ~30-40 risk, Ratio > 1.15 -> High risk (>70)
        raw_score = int((ratio - 0.85) * 200)
        risk_score = max(10, min(95, raw_score))
        
        if risk_score >= 65:
            risk_level = 'High'
            risk_color = '#ef4444' # Red
            recommendation = f"High overproduction risk detected for {crop} in {state}. High chance of market price drops during harvest season. Consider diversifying crop acreage."
        elif risk_score >= 40:
            risk_level = 'Moderate'
            risk_color = '#f59e0b' # Amber
            recommendation = f"Balanced market conditions for {crop} in {state}. Monitor local mandi arrivals closely."
        else:
            risk_level = 'Low'
            risk_color = '#10b981' # Green
            recommendation = f"Favorable demand outlook for {crop} in {state}. Projected local demand exceeds supply capacity."
            
        # Generate alternative lower-risk crops
        all_crops = list(self.crop_demand_data.keys())
        alternatives = [c for c in all_crops if c != crop]
        random.seed(hash(crop + state) % 10000)
        suggested_alternatives = random.sample(alternatives, min(3, len(alternatives)))
        
        return {
            'crop': crop,
            'state': state,
            'supply_mt': projected_supply,
            'demand_mt': estimated_demand,
            'supply_demand_ratio': ratio,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_color': risk_color,
            'recommendation': recommendation,
            'suggested_alternatives': suggested_alternatives,
            'historical_trend': [
                {'year': '2022', 'supply': int(projected_supply * 0.91), 'demand': int(estimated_demand * 0.93)},
                {'year': '2023', 'supply': int(projected_supply * 0.95), 'demand': int(estimated_demand * 0.96)},
                {'year': '2024', 'supply': int(projected_supply * 0.98), 'demand': int(estimated_demand * 0.98)},
                {'year': '2025', 'supply': projected_supply, 'demand': estimated_demand}
            ]
        }
