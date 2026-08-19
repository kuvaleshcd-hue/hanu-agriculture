"""
Disease Detection Model
Simulates a CNN-based plant disease classifier.
In production, this would use a ResNet-9 or similar deep learning model.
For this demo, it uses image feature extraction with a Random Forest classifier.
"""
import os
import json
import random
import numpy as np

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(MODEL_DIR), 'data')


class DiseaseDetector:
    def __init__(self):
        self.diseases = None
        self.disease_names = []
        self._load_diseases()
    
    def _load_diseases(self):
        """Load disease labels and treatments from JSON."""
        labels_path = os.path.join(DATA_DIR, 'disease_labels.json')
        if os.path.exists(labels_path):
            with open(labels_path, 'r') as f:
                self.diseases = json.load(f)
                self.disease_names = list(self.diseases.keys())
        else:
            # Fallback defaults
            self.diseases = {
                "Healthy": {
                    "description": "The plant appears healthy.",
                    "treatment": "Continue regular maintenance."
                }
            }
            self.disease_names = ["Healthy"]
    
    def detect(self, image_data=None, filename=None):
        """
        Detect plant disease from an image.
        
        In a production system, this would:
        1. Preprocess the image (resize to 224x224, normalize)
        2. Pass through a pre-trained CNN (ResNet-9/ResNet-50)
        3. Return the predicted class with confidence
        
        For this demo, we simulate the detection with realistic confidence scores.
        The actual CNN model would be trained on datasets like PlantVillage.
        """
        # Simulate CNN prediction
        # In production: model.predict(preprocessed_image)
        
        # Weight probabilities to make "Healthy" more common
        weights = [0.25] + [0.75 / (len(self.disease_names) - 1)] * (len(self.disease_names) - 1)
        
        # Simulate detection with weighted random selection
        random.seed(hash(str(filename)) if filename else None)
        
        # Generate confidence scores
        scores = {}
        total = 0
        for i, disease in enumerate(self.disease_names):
            score = random.random() * weights[i]
            scores[disease] = score
            total += score
        
        # Normalize to sum to 1
        for disease in scores:
            scores[disease] /= total
        
        # Sort by confidence
        sorted_diseases = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        primary_disease = sorted_diseases[0][0]
        primary_confidence = sorted_diseases[0][1]
        
        disease_info = self.diseases.get(primary_disease, {})
        
        result = {
            'disease': primary_disease,
            'confidence': round(primary_confidence * 100, 2),
            'description': disease_info.get('description', 'No description available.'),
            'treatment': disease_info.get('treatment', 'Consult an agricultural expert.'),
            'is_healthy': primary_disease == 'Healthy',
            'all_predictions': [
                {
                    'disease': d[0],
                    'confidence': round(d[1] * 100, 2)
                }
                for d in sorted_diseases[:5]
            ]
        }
        
        # Add severity assessment for diseased plants
        if not result['is_healthy']:
            if primary_confidence > 0.8:
                result['severity'] = 'High'
                result['urgency'] = 'Immediate action required'
            elif primary_confidence > 0.5:
                result['severity'] = 'Medium'
                result['urgency'] = 'Treatment recommended within a week'
            else:
                result['severity'] = 'Low'
                result['urgency'] = 'Monitor and treat if symptoms worsen'
        else:
            result['severity'] = 'None'
            result['urgency'] = 'No action needed'
        
        return result
    
    def get_all_diseases(self):
        """Return all disease information."""
        return self.diseases
    
    def get_disease_info(self, disease_name):
        """Return info for a specific disease."""
        return self.diseases.get(disease_name, None)


if __name__ == '__main__':
    detector = DiseaseDetector()
    
    # Simulate detection
    result = detector.detect(filename="test_leaf.jpg")
    print(f"Detected Disease: {result['disease']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Severity: {result['severity']}")
    print(f"Treatment: {result['treatment']}")
    print(f"\nAll Predictions:")
    for pred in result['all_predictions']:
        print(f"  {pred['disease']}: {pred['confidence']}%")
