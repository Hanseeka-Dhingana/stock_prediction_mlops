import os
import sys
import pandas as pd
import wandb
from dotenv import load_dotenv

# Models
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, VotingRegressor
from xgboost import XGBRegressor

# Metric & Helpers
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from src.utils import pull_from_feature_store

# Load Environment Variables (API Key)
load_dotenv()

# DEFINE THE SEARCH SPACE (The "Menu" of options)
sweep_config = {
    'method': 'bayes',  # "Bayesian" means it learns from previous runs to find the best faster
    'metric': {
        'name': 'mae',
        'goal': 'minimize'   # We want the LOWEST error
    },
    'parameters': {
        # Random Forest Params
        'rf_n_estimators': {'values': [50, 100, 200]},
        'rf_max_depth': {'values': [10, 20, None]},
        
        # XGBoost Params
        'xgb_learning_rate': {'values': [0.01, 0.1, 0.2]},
        'xgb_n_estimators': {'values': [50, 100, 200]}
    }
}

def train_sweep():
    # Initialize a new W&B run
    with wandb.init():
        config = wandb.config
        
        # Load Data
        try:
            df = pull_from_feature_store()
        except Exception:
            return

        X = df[['Close', 'SMA_10', 'SMA_50', 'Volatility']]
        y = df['Target']

        # Split & Scale
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Define Models using W&B Config
        lr = LinearRegression()
        
        rf = RandomForestRegressor(
            n_estimators=config.rf_n_estimators, 
            max_depth=config.rf_max_depth,
            random_state=42
        )
        
        xgb = XGBRegressor(
            n_estimators=config.xgb_n_estimators, 
            learning_rate=config.xgb_learning_rate, 
            random_state=42
        )

        # Ensemble
        ensemble = VotingRegressor(estimators=[('lr', lr), ('rf', rf), ('xgb', xgb)])

        # Train
        ensemble.fit(X_train_scaled, y_train.values.ravel())
    
        # Evaluate
        preds = ensemble.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, preds)
        
        # Log Result
        wandb.log({"mae": mae})
        print(f"Params: RF={config.rf_n_estimators} XGB_LR={config.xgb_learning_rate} -> MAE: {mae:.2f}")

if __name__ == "__main__":
    # Login
    wandb.login(key=os.getenv("WANDB_API_KEY"))
    
    # Create the Sweep (Controller)
    sweep_id = wandb.sweep(sweep_config, project="stock-prediction-prod")
    
    print(f"Sweep Created with ID: {sweep_id}")
    print("starting the agent to run 10 experiments...")
    
    # Run the Agent (It will run the train_sweep function 10 times)
    wandb.agent(sweep_id, train_sweep, count=10)