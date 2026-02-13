import os
import sys
import pandas as pd
import wandb  
from dataclasses import dataclass

# Models
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, VotingRegressor
from xgboost import XGBRegressor

# Sklearn helpers
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Our custom helpers
from src.utils import save_object, pull_from_feature_store


@dataclass
class ModelTrainerConfig:
    # save these files locally first
    trained_model_file_path = os.path.join("models", "model.pkl")
    scaler_file_path = os.path.join("models", "scaler.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self):
        print("Starting Model Training & Registry...")
        
        # INITIALIZE W&B RUN
        # This tells W&B: "I am starting a training job"
        run = wandb.init(project="stock-prediction-prod", job_type="train_and_register")
        
        try:
            # LOAD DATA FROM MONGO 
            df = pull_from_feature_store()
            
            X = df[['Close', 'SMA_10', 'SMA_50', 'Volatility']]
            y = df['Target']
            
            # SPLIT & SCALE 
            # Shuffle=False is mandatory for Time Series
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
            
            print("   Scaling Data...")
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # DEFINE ENSEMBLE MODEL 
            # Combine the 3 best models that found in EDA
            lr = LinearRegression()
            rf = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
            xgb = XGBRegressor(n_estimators=200, learning_rate=0.2, random_state=42)
            
            ensemble = VotingRegressor(estimators=[
                ('lr', lr), ('rf', rf), ('xgb', xgb)
            ])
            
            # TRAIN
            print("   Training Ensemble Model...")
            ensemble.fit(X_train_scaled, y_train.values.ravel())
            
            # EVALUATE 
            preds = ensemble.predict(X_test_scaled)
            mae = mean_absolute_error(y_test, preds)
            r2 = r2_score(y_test, preds)
            
            print(f"Final Performance -> MAE: ${mae:.2f} | R2: {r2:.4f}")
            
            # Log metrics to W&B dashboard so I can compare versions later
            wandb.log({"mae": mae, "r2": r2})

            # SAVE LOCALLY
            save_object(self.model_trainer_config.trained_model_file_path, ensemble)
            save_object(self.model_trainer_config.scaler_file_path, scaler)
            print("Model saved locally to artifacts/")

            # Model Registery 
            print(" Registering Model to W&B Artifacts...")
            
            # 1. Create an artifacts (A virtual box)
            # "stock_prediction_model" is the REGISTRY NAME.
            # W&B will automatically handle versioning (v0, v1, v2) for this name.
            artifact = wandb.Artifact(
                name="stock_prediction_model", 
                type="model",
                description="Voting Ensemble (LR+RF+XGB)",
                metadata={"mae": mae, "r2": r2}
            )
            
            # 2. Put our local model file into the box
            artifact.add_file(self.model_trainer_config.trained_model_file_path)
            
            # 3. Put the Scaler into the box (We need this for the App too!)
            artifact.add_file(self.model_trainer_config.scaler_file_path)

            # 4. Upload the box to W&B Cloud
            run.log_artifact(artifact)
            
            print("Model successfully registered in W&B Cloud!")
            # ---------------------------------------------------------

            wandb.finish()

        except Exception as e:
            wandb.finish() # Close run even if it fails
            raise Exception(e)

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.initiate_model_trainer()