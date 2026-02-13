from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn
import os

# INITIALIZE APP
app = FastAPI(
    title="Stock Prediction API",
    description="Backend using Linear+RF+XGB Ensemble",
    version="1.0"
)

# LOAD ARTIFACTS (Model & Scaler)
# We use relative paths to find the artifacts folder
curr_dir = os.path.dirname(os.path.realpath(__file__))
# Going up one level from 'api/' to root, then into 'artifacts/'
artifact_path = os.path.join(curr_dir, "..", "models")

model_path = os.path.join(artifact_path, "model.pkl")
scaler_path = os.path.join(artifact_path, "scaler.pkl")

# Fail fast if files are missing
if not os.path.exists(model_path):
    raise RuntimeError(f"Model not found at {model_path}. Did you train it?")

print(f"Loading model from: {model_path}")
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# DEFINE INPUT DATA SCHEMA
# This forces the user to send exactly these 4 numbers
class StockRequest(BaseModel):
    Close: float
    SMA_10: float
    SMA_50: float
    Volatility: float

# PREDICTION ENDPOINT
@app.post("/predict")
def predict(data: StockRequest):
    try:
        # Convert JSON input to DataFrame
        df = pd.DataFrame([data.dict()])
        
        # Scale the data (Critical step!)
        scaled_data = scaler.transform(df)
        
        # Predict
        prediction = model.predict(scaled_data)
        
        return {
            "predicted_price": float(prediction[0]),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# HEALTH CHECK (For Railway/Docker)
@app.get("/")
def health_check():
    return {"status": "ok", "message": "Stock API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)