"""
Crop Recommendation Model
Uses Random Forest Classifier to predict the best crop based on soil and weather parameters.
"""
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(MODEL_DIR), 'data')

class CropRecommender:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        self.model_path = os.path.join(MODEL_DIR, 'crop_model.pkl')
        self.scaler_path = os.path.join(MODEL_DIR, 'crop_scaler.pkl')
    
    def train(self):
        """Train the Random Forest model on crop dataset."""
        data_path = os.path.join(DATA_DIR, 'crop_data.csv')
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Crop data not found at {data_path}. Run generate_datasets.py first.")
        
        df = pd.read_csv(data_path)
        X = df[self.feature_names].values
        y = df['label'].values
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train_scaled, y_train)
        
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Crop Recommendation Model Accuracy: {accuracy:.4f}")
        
        # Save model and scaler
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        with open(self.scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        return accuracy
    
    def load(self):
        """Load pre-trained model and scaler."""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(self.scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            return True
        return False
    
    def predict(self, n, p, k, temperature, humidity, ph, rainfall):
        """Predict the best crops with confidence scores."""
        if self.model is None:
            if not self.load():
                self.train()
        
        features = np.array([[n, p, k, temperature, humidity, ph, rainfall]])
        features_scaled = self.scaler.transform(features)
        
        # Get probability scores for all crops
        probabilities = self.model.predict_proba(features_scaled)[0]
        classes = self.model.classes_
        
        # Sort by probability and return top 5
        sorted_indices = np.argsort(probabilities)[::-1]
        recommendations = []
        for idx in sorted_indices[:5]:
            recommendations.append({
                'crop': classes[idx],
                'confidence': round(float(probabilities[idx]) * 100, 2)
            })
        
        return recommendations


if __name__ == '__main__':
    recommender = CropRecommender()
    accuracy = recommender.train()
    
    # Test prediction
    result = recommender.predict(
        n=90, p=42, k=43, temperature=24.5,
        humidity=82, ph=6.5, rainfall=200
    )
    print("\nSample Prediction (N=90, P=42, K=43, Temp=24.5, Humidity=82, pH=6.5, Rainfall=200):")
    for r in result:
        print(f"  {r['crop']}: {r['confidence']}%")
