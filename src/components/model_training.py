import os
import sys
import pandas as pd
from dataclasses import dataclass
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Import helpers
from src.utils import save_object, pull_from_feature_store

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")
    scaler_file_path = os.path.join("artifacts", "scaler.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self):
        print("Starting Model Training Component...")
        try:
            # PULL DATA FROM FEATURE STORE (MongoDB)
            df = pull_from_feature_store()
            
            # DEFINE X and y
            feature_cols = ['Close', 'SMA_10', 'SMA_50', 'Volatility']
            target_col = 'Target'
            
            X = df[feature_cols]
            y = df[target_col]
            
            # TRAIN-TEST SPLIT
            # shuffle=False is MANDATORY for time series
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
            
            # SCALING
            print("   Scaling Data...")
            scaler = StandardScaler()
            
            # Fit on Train ONLY (Learn from Past)
            scaler.fit(X_train)
            
            # Transform both
            X_train_scaled = scaler.transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # TRAIN MODEL
            print("   Training Linear Regression Model...")
            model = LinearRegression()
            
            # Flatten y_train (convert column to list)
            model.fit(X_train_scaled, y_train.values.ravel())
            
            # EVALUATE
            preds = model.predict(X_test_scaled)
            mae = mean_absolute_error(y_test, preds)
            r2 = r2_score(y_test, preds)
            print(f"Model Performance -> MAE: ${mae:.2f} | R2: {r2:.4f}")

            # SAVE ARTIFACTS
            save_object(self.model_trainer_config.trained_model_file_path, model)
            save_object(self.model_trainer_config.scaler_file_path, scaler)
            
            print(f"Model & Scaler saved to artifacts/")

        except Exception as e:
            raise Exception(e)

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.initiate_model_trainer()