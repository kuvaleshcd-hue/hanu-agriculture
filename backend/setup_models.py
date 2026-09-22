import os
import sys

def setup():
    print("🌾 Starting Agricultural AI Model Setup...")
    
    # 1. Generate datasets
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    if not os.path.exists(os.path.join(data_dir, 'crop_data.csv')):
        print("📊 Generating datasets for the first time...")
        import subprocess
        subprocess.run([sys.executable, os.path.join(data_dir, 'generate_datasets.py')])
        print("✅ Datasets generated!")
    else:
        print("✅ Datasets already exist!")

    # 2. Train models
    from models.crop_recommendation import CropRecommender
    from models.fertilizer_recommendation import FertilizerRecommender
    from models.price_prediction import PricePredictor

    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
    if not os.path.exists(os.path.join(models_dir, 'crop_model.pkl')):
        print("🧠 Training ML models for the first time...")
        
        crop_recommender = CropRecommender()
        crop_recommender.train()
        
        fertilizer_recommender = FertilizerRecommender()
        fertilizer_recommender.train()
        
        price_predictor = PricePredictor()
        price_predictor.train()
        
        print("✅ All models trained!")
    else:
        print("✅ Pre-trained models already exist!")

if __name__ == '__main__':
    setup()
