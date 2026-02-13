import os
import wandb
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("WANDB_API_KEY")
if api_key:
    wandb.login(key=api_key)

# Login to W&B
api = wandb.Api(timeout=60)

# Get the Sweep
sweep = api.sweep("hanseeka-dhingana-sukkur-iba-university/stock-prediction-prod/sweeps/rpev57yx")

# Get all Runs
runs = sweep.runs

# Extract Data
summary_list = []
for run in runs:
    # .summary contains the output metrics (MAE, R2)
    # .config contains the hyperparameters (RF_n_estimators, etc)
    # .name is the run name (e.g., astral-paper-13)
    run_data = {
        "name": run.name, 
        **run.summary._json_dict, 
        **run.config
    }
    summary_list.append(run_data)

# Save to CSV
df = pd.DataFrame(summary_list)
df.to_csv("sweep_results.csv", index=False)

print("Successfully saved sweep results to sweep_results.csv")