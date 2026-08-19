"""
Price / Demand Prediction Model
Uses Gradient Boosting Regressor to forecast agricultural commodity prices.
Includes time-series feature engineering for seasonal trends.
"""
import os
import pickle
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import math

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(MODEL_DIR), 'data')


class PricePredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.commodity_encoder = LabelEncoder()
        self.state_encoder = LabelEncoder()
        self.model_path = os.path.join(MODEL_DIR, 'price_model.pkl')
        self.encoders_path = os.path.join(MODEL_DIR, 'price_encoders.pkl')
        self.df = None
    
    def _engineer_features(self, df):
        """Create time-series features from date column."""
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day_of_year'] = df['date'].dt.dayofyear
        df['day_of_week'] = df['date'].dt.dayofweek
        df['quarter'] = df['date'].dt.quarter
        
        # Cyclical encoding for month and day_of_year
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        df['doy_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
        df['doy_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
        
        return df
    
    def train(self):
        """Train the Gradient Boosting model on price dataset."""
        data_path = os.path.join(DATA_DIR, 'price_data.csv')
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Price data not found. Run generate_datasets.py first.")
        
        df = pd.read_csv(data_path)
        self.df = df.copy()
        
        df = self._engineer_features(df)
        
        # Encode categorical features
        df['commodity_enc'] = self.commodity_encoder.fit_transform(df['commodity'])
        df['state_enc'] = self.state_encoder.fit_transform(df['state'])
        
        feature_cols = ['commodity_enc', 'state_enc', 'year', 'month',
                        'month_sin', 'month_cos', 'doy_sin', 'doy_cos',
                        'quarter', 'day_of_week']
        
        X = df[feature_cols].values
        y = df['modal_price'].values
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model = GradientBoostingRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            min_samples_split=5,
            min_samples_leaf=3,
            random_state=42
        )
        self.model.fit(X_train_scaled, y_train)
        
        y_pred = self.model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"Price Prediction Model - MAE: ₹{mae:.2f}, R²: {r2:.4f}")
        
        # Save model and encoders
        with open(self.model_path, 'wb') as f:
            pickle.dump((self.model, self.scaler), f)
        with open(self.encoders_path, 'wb') as f:
            pickle.dump({
                'commodity': self.commodity_encoder,
                'state': self.state_encoder
            }, f)
        
        return {'mae': mae, 'r2': r2}
    
    def load(self):
        """Load pre-trained model and encoders."""
        if os.path.exists(self.model_path) and os.path.exists(self.encoders_path):
            with open(self.model_path, 'rb') as f:
                self.model, self.scaler = pickle.load(f)
            with open(self.encoders_path, 'rb') as f:
                encoders = pickle.load(f)
                self.commodity_encoder = encoders['commodity']
                self.state_encoder = encoders['state']
            return True
        return False
    
    def predict_future(self, commodity, state, days=30):
        """Predict prices for the next N days."""
        if self.model is None:
            if not self.load():
                self.train()
        
        # Encode inputs
        try:
            commodity_enc = self.commodity_encoder.transform([commodity])[0]
        except ValueError:
            return {'error': f'Unknown commodity: {commodity}'}
        
        try:
            state_enc = self.state_encoder.transform([state])[0]
        except ValueError:
            return {'error': f'Unknown state: {state}'}
        
        today = datetime.now()
        predictions = []
        
        for i in range(days):
            future_date = today + timedelta(days=i)
            month = future_date.month
            year = future_date.year
            doy = future_date.timetuple().tm_yday
            dow = future_date.weekday()
            quarter = (month - 1) // 3 + 1
            
            month_sin = math.sin(2 * math.pi * month / 12)
            month_cos = math.cos(2 * math.pi * month / 12)
            doy_sin = math.sin(2 * math.pi * doy / 365)
            doy_cos = math.cos(2 * math.pi * doy / 365)
            
            features = np.array([[commodity_enc, state_enc, year, month,
                                  month_sin, month_cos, doy_sin, doy_cos,
                                  quarter, dow]])
            features_scaled = self.scaler.transform(features)
            
            predicted_price = float(self.model.predict(features_scaled)[0])
            
            predictions.append({
                'date': future_date.strftime('%Y-%m-%d'),
                'predicted_price': round(predicted_price, 2),
                'min_price': round(predicted_price * 0.92, 2),
                'max_price': round(predicted_price * 1.08, 2)
            })
        
        # Calculate trend summary
        if len(predictions) >= 2:
            start_price = predictions[0]['predicted_price']
            end_price = predictions[-1]['predicted_price']
            change_pct = ((end_price - start_price) / start_price) * 100
            trend = 'rising' if change_pct > 2 else ('falling' if change_pct < -2 else 'stable')
        else:
            change_pct = 0
            trend = 'stable'
        
        return {
            'commodity': commodity,
            'state': state,
            'forecast_days': days,
            'predictions': predictions,
            'summary': {
                'avg_price': round(np.mean([p['predicted_price'] for p in predictions]), 2),
                'min_price': round(min(p['min_price'] for p in predictions), 2),
                'max_price': round(max(p['max_price'] for p in predictions), 2),
                'trend': trend,
                'change_percent': round(change_pct, 2)
            }
        }
    
    def get_historical(self, commodity, state, days=90):
        """Get historical price data for a commodity in a state."""
        data_path = os.path.join(DATA_DIR, 'price_data.csv')
        if self.df is None:
            if os.path.exists(data_path):
                self.df = pd.read_csv(data_path)
            else:
                return []
        
        filtered = self.df[
            (self.df['commodity'] == commodity) &
            (self.df['state'] == state)
        ].sort_values('date').tail(days)
        
        return filtered[['date', 'modal_price', 'min_price', 'max_price']].to_dict('records')
    
    def get_commodities(self):
        """Return available commodities."""
        if hasattr(self.commodity_encoder, 'classes_'):
            return list(self.commodity_encoder.classes_)
        return ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Groundnut',
                'Soybean', 'Onion', 'Tomato', 'Potato', 'Banana', 'Mango',
                'Coconut', 'Coffee', 'Turmeric']
    
    def get_states(self):
        """Return available states."""
        if hasattr(self.state_encoder, 'classes_'):
            return list(self.state_encoder.classes_)
        return ['Karnataka', 'Maharashtra', 'Tamil Nadu', 'Andhra Pradesh', 'Kerala',
                'Uttar Pradesh', 'Madhya Pradesh', 'Gujarat', 'Rajasthan', 'Punjab']


if __name__ == '__main__':
    predictor = PricePredictor()
    metrics = predictor.train()
    
    # Test prediction
    result = predictor.predict_future('Rice', 'Karnataka', days=7)
    print(f"\n7-Day Rice Price Forecast for Karnataka:")
    print(f"Trend: {result['summary']['trend']} ({result['summary']['change_percent']:+.2f}%)")
    for p in result['predictions']:
        print(f"  {p['date']}: ₹{p['predicted_price']}")
