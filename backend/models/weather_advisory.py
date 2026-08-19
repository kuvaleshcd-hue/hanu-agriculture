"""
Smart Weather & Precision Irrigation Advisory Engine
Fetches 7-day live/simulated weather forecasts across Indian agricultural districts,
computes crop water requirement (ET₀), and generates pest risk warnings.
"""
import urllib.request
import json
import random
import os

class WeatherAdvisoryEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('WEATHER_API_KEY')
        # Default district coordinate mappings for major Indian states
        self.state_coords = {
            'Karnataka': {'city': 'Bengaluru', 'lat': 12.97, 'lon': 77.59},
            'Maharashtra': {'city': 'Pune', 'lat': 18.52, 'lon': 73.85},
            'Uttar Pradesh': {'city': 'Lucknow', 'lat': 26.84, 'lon': 80.94},
            'Punjab': {'city': 'Ludhiana', 'lat': 30.90, 'lon': 75.85},
            'Haryana': {'city': 'Karnal', 'lat': 29.68, 'lon': 76.99},
            'Madhya Pradesh': {'city': 'Indore', 'lat': 22.71, 'lon': 75.85},
            'Gujarat': {'city': 'Rajkot', 'lat': 22.30, 'lon': 70.80},
            'Tamil Nadu': {'city': 'Coimbatore', 'lat': 11.01, 'lon': 76.95},
            'Andhra Pradesh': {'city': 'Guntur', 'lat': 16.30, 'lon': 80.43},
            'West Bengal': {'city': 'Burdwan', 'lat': 23.23, 'lon': 87.86}
        }

    def get_advisory(self, state='Karnataka', api_key=None):
        state = state.title() if state else 'Karnataka'
        coords = self.state_coords.get(state, {'city': 'Bengaluru', 'lat': 12.97, 'lon': 77.59})
        key = api_key or self.api_key
        
        forecast = None
        
        # 1. Try WeatherAPI.com if API Key is provided
        if key:
            try:
                url = f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={coords['lat']},{coords['lon']}&days=7&aqi=no"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=4) as resp:
                    data = json.loads(resp.read().decode())
                    days = data.get('forecast', {}).get('forecastday', [])
                    forecast = []
                    for d in days:
                        day_data = d.get('day', {})
                        forecast.append({
                            'date': d.get('date'),
                            'max_temp': day_data.get('maxtemp_c', 30),
                            'min_temp': day_data.get('mintemp_c', 20),
                            'rain_mm': day_data.get('totalprecip_mm', 0),
                            'humidity_pct': day_data.get('avghumidity', 65)
                        })
            except Exception as e:
                print(f"WeatherAPI.com fetch failed, using fallback: {e}")

        # 2. Try Open-Meteo free API if no key or key request failed
        if not forecast:
            try:
                url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_mean&timezone=auto"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=3) as resp:
                    data = json.loads(resp.read().decode())
                    daily = data.get('daily', {})
                    dates = daily.get('time', [])
                    temp_max = daily.get('temperature_2m_max', [])
                    temp_min = daily.get('temperature_2m_min', [])
                    precip = daily.get('precipitation_sum', [])
                    humidity = daily.get('relative_humidity_2m_mean', [])
                    
                    forecast = []
                    for i in range(min(7, len(dates))):
                        forecast.append({
                            'date': dates[i],
                            'max_temp': temp_max[i],
                            'min_temp': temp_min[i],
                            'rain_mm': precip[i],
                            'humidity_pct': humidity[i] if i < len(humidity) else 65
                        })
            except Exception as e:
                print(f"Open-Meteo API fallback for {state}: {e}")
                forecast = self._generate_fallback_forecast()

        # Compute today's weather metrics
        today = forecast[0]
        avg_temp = round((today['max_temp'] + today['min_temp']) / 2, 1)
        rain_total = sum(d['rain_mm'] for d in forecast)
        
        # Evapotranspiration Water Needs (ET₀ estimation in mm/day)
        et0 = round(0.0023 * (avg_temp + 17.8) * (today['max_temp'] - today['min_temp'])**0.5 * 3.5, 1)
        water_needed_liters_per_acre = int(et0 * 4046.86) # 1 mm = 4046.86 liters/acre
        
        # Pest & Disease Risk Assessment
        if today['humidity_pct'] > 75 and avg_temp > 24:
            pest_risk = 'High'
            pest_warning = "High humidity & warm temperatures create ideal conditions for Fungal Blight and Aphids. Inspect leaves immediately."
        elif today['humidity_pct'] > 60:
            pest_risk = 'Moderate'
            pest_warning = "Moderate humidity. Regular field monitoring recommended for early pest signs."
        else:
            pest_risk = 'Low'
            pest_warning = "Low humidity & dry weather reduce fungal risk. Keep soil adequately irrigated."
            
        # Actionable Irrigation & Spraying Guidance
        if today['rain_mm'] > 5.0:
            irrigation_advice = "Heavy rainfall expected today. Suspend automated irrigation and ensure field drainage."
            spraying_advice = "Do NOT apply pesticides or liquid fertilizers today — risk of rain wash-off."
        elif rain_total > 15.0:
            irrigation_advice = f"Rainfall predicted this week ({round(rain_total, 1)} mm). Light irrigation only."
            spraying_advice = "Plan chemical spraying during dry morning windows."
        else:
            irrigation_advice = f"Dry conditions. Apply ~{water_needed_liters_per_acre:,} Liters/acre of drip/sprinkler irrigation."
            spraying_advice = "Favorable weather for foliar spray applications."

        return {
            'state': state,
            'city': coords['city'],
            'current_temp': avg_temp,
            'max_temp': today['max_temp'],
            'min_temp': today['min_temp'],
            'humidity': today['humidity_pct'],
            'rain_today_mm': today['rain_mm'],
            'weekly_rain_total_mm': round(rain_total, 1),
            'water_requirement_et0_mm': et0,
            'water_needed_liters_per_acre': water_needed_liters_per_acre,
            'pest_risk': pest_risk,
            'pest_warning': pest_warning,
            'irrigation_advice': irrigation_advice,
            'spraying_advice': spraying_advice,
            '7day_forecast': forecast
        }

    def _generate_fallback_forecast(self):
        import datetime
        base_date = datetime.date.today()
        forecast = []
        for i in range(7):
            d = base_date + datetime.timedelta(days=i)
            t_max = round(random.uniform(28.0, 35.0), 1)
            t_min = round(t_max - random.uniform(8.0, 12.0), 1)
            rain = round(random.choice([0.0, 0.0, 0.0, 2.5, 8.0, 14.0]), 1)
            hum = random.randint(55, 80)
            forecast.append({
                'date': d.strftime('%Y-%m-%d'),
                'max_temp': t_max,
                'min_temp': t_min,
                'rain_mm': rain,
                'humidity_pct': hum
            })
        return forecast
