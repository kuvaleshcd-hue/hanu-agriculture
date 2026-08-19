"""
Fertilizer Recommendation Model
Uses Decision Tree Classifier to recommend fertilizers based on soil composition and crop type.
"""
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(MODEL_DIR), 'data')


# Fertilizer application guidance
FERTILIZER_GUIDANCE = {
    'NPK 20-20-20': {
        'usage': 'Apply 100-150 kg/hectare during sowing. Split application: 50% at sowing, 50% at flowering.',
        'benefits': 'Balanced nutrition for overall growth. Ideal for nutrient-deficient soils.',
        'precautions': 'Do not mix with alkaline materials. Store in dry conditions.'
    },
    'DAP (Diammonium Phosphate)': {
        'usage': 'Apply 100-125 kg/hectare as basal dose before sowing.',
        'benefits': 'High phosphorus content promotes root development and early maturity.',
        'precautions': 'Avoid direct contact with seeds. Best applied in slightly acidic soils.'
    },
    'MOP (Muriate of Potash)': {
        'usage': 'Apply 50-100 kg/hectare. Can be applied at sowing or top-dressed.',
        'benefits': 'Improves disease resistance, water regulation, and crop quality.',
        'precautions': 'Avoid in chloride-sensitive crops like tobacco and potato.'
    },
    'Urea': {
        'usage': 'Apply 100-200 kg/hectare in 2-3 split doses during growth stages.',
        'benefits': 'Highest nitrogen content (46%). Promotes vegetative growth and green color.',
        'precautions': 'Apply when soil is moist. Avoid surface broadcasting to reduce nitrogen loss.'
    },
    'SSP (Single Super Phosphate)': {
        'usage': 'Apply 200-300 kg/hectare as basal dose before transplanting.',
        'benefits': 'Provides phosphorus, calcium, and sulfur. Good for oilseed crops.',
        'precautions': 'Do not mix with urea or calcium ammonium nitrate.'
    },
    'Balanced NPK 10-10-10': {
        'usage': 'Apply 200-300 kg/hectare. Suitable for maintenance fertilization.',
        'benefits': 'Gentle, balanced feeding for crops with moderate nutrient needs.',
        'precautions': 'May not be sufficient for heavy-feeding crops. Supplement as needed.'
    },
    'No Fertilizer Needed': {
        'usage': 'Soil nutrients are sufficient. No additional fertilizer required at this time.',
        'benefits': 'Saves cost. Prevents over-fertilization and environmental damage.',
        'precautions': 'Re-test soil after harvest. Monitor crop health for any deficiency signs.'
    },
}


class FertilizerRecommender:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.soil_encoder = LabelEncoder()
        self.crop_encoder = LabelEncoder()
        self.fert_encoder = LabelEncoder()
        self.model_path = os.path.join(MODEL_DIR, 'fertilizer_model.pkl')
        self.encoders_path = os.path.join(MODEL_DIR, 'fertilizer_encoders.pkl')
    
    def train(self):
        """Train the Decision Tree model on fertilizer dataset."""
        data_path = os.path.join(DATA_DIR, 'fertilizer_data.csv')
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Fertilizer data not found. Run generate_datasets.py first.")
        
        df = pd.read_csv(data_path)
        
        # Encode categorical features
        df['soil_encoded'] = self.soil_encoder.fit_transform(df['soil_type'])
        df['crop_encoded'] = self.crop_encoder.fit_transform(df['crop_type'])
        df['fert_encoded'] = self.fert_encoder.fit_transform(df['fertilizer'])
        
        feature_cols = ['temperature', 'humidity', 'moisture', 'soil_encoded', 'crop_encoded',
                        'nitrogen', 'phosphorous', 'potassium']
        
        X = df[feature_cols].values
        y = df['fert_encoded'].values
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model = DecisionTreeClassifier(
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        self.model.fit(X_train_scaled, y_train)
        
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Fertilizer Recommendation Model Accuracy: {accuracy:.4f}")
        
        # Save model and encoders
        with open(self.model_path, 'wb') as f:
            pickle.dump((self.model, self.scaler), f)
        with open(self.encoders_path, 'wb') as f:
            pickle.dump({
                'soil': self.soil_encoder,
                'crop': self.crop_encoder,
                'fert': self.fert_encoder
            }, f)
        
        return accuracy
    
    def load(self):
        """Load pre-trained model and encoders."""
        if os.path.exists(self.model_path) and os.path.exists(self.encoders_path):
            with open(self.model_path, 'rb') as f:
                self.model, self.scaler = pickle.load(f)
            with open(self.encoders_path, 'rb') as f:
                encoders = pickle.load(f)
                self.soil_encoder = encoders['soil']
                self.crop_encoder = encoders['crop']
                self.fert_encoder = encoders['fert']
            return True
        return False
    
    def predict(self, temperature, humidity, moisture, soil_type, crop_type, nitrogen, phosphorous, potassium):
        """Predict the recommended fertilizer with guidance."""
        if self.model is None:
            if not self.load():
                self.train()
        
        # Encode categorical inputs
        try:
            soil_enc = self.soil_encoder.transform([soil_type])[0]
        except ValueError:
            soil_enc = 0  # default
        
        try:
            crop_enc = self.crop_encoder.transform([crop_type])[0]
        except ValueError:
            crop_enc = 0  # default
        
        features = np.array([[temperature, humidity, moisture, soil_enc, crop_enc,
                              nitrogen, phosphorous, potassium]])
        features_scaled = self.scaler.transform(features)
        
        pred_encoded = self.model.predict(features_scaled)[0]
        fertilizer_name = self.fert_encoder.inverse_transform([pred_encoded])[0]
        
        guidance = FERTILIZER_GUIDANCE.get(fertilizer_name, {
            'usage': 'Follow manufacturer instructions.',
            'benefits': 'Provides essential nutrients.',
            'precautions': 'Apply as recommended.'
        })
        
        # Nutrient analysis
        analysis = []
        if nitrogen < 40:
            analysis.append("⚠️ Nitrogen is LOW — consider nitrogen-rich supplements.")
        elif nitrogen > 100:
            analysis.append("⚡ Nitrogen is HIGH — reduce nitrogen-based fertilizers.")
        else:
            analysis.append("✅ Nitrogen level is optimal.")
        
        if phosphorous < 40:
            analysis.append("⚠️ Phosphorous is LOW — phosphate supplements recommended.")
        elif phosphorous > 80:
            analysis.append("⚡ Phosphorous is HIGH — avoid phosphate fertilizers.")
        else:
            analysis.append("✅ Phosphorous level is optimal.")
        
        if potassium < 30:
            analysis.append("⚠️ Potassium is LOW — potash supplements recommended.")
        elif potassium > 80:
            analysis.append("⚡ Potassium is HIGH — reduce potash-based fertilizers.")
        else:
            analysis.append("✅ Potassium level is optimal.")
        
        return {
            'fertilizer': fertilizer_name,
            'guidance': guidance,
            'nutrient_analysis': analysis,
            'soil_type': soil_type,
            'crop_type': crop_type
        }
    
    def get_soil_types(self):
        """Return available soil types."""
        return ['Sandy', 'Loamy', 'Black', 'Red', 'Clayey']
    
    def get_crop_types(self):
        """Return available crop types."""
        if hasattr(self.crop_encoder, 'classes_'):
            return list(self.crop_encoder.classes_)
        return ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Coffee',
                'Coconut', 'Groundnut', 'Banana', 'Mango']


if __name__ == '__main__':
    recommender = FertilizerRecommender()
    accuracy = recommender.train()
    
    result = recommender.predict(
        temperature=28, humidity=65, moisture=40,
        soil_type='Loamy', crop_type='Rice',
        nitrogen=30, phosphorous=50, potassium=40
    )
    print(f"\nRecommended Fertilizer: {result['fertilizer']}")
    print(f"Usage: {result['guidance']['usage']}")
    for note in result['nutrient_analysis']:
        print(f"  {note}")
