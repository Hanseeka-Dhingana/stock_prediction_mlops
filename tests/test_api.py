from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_api_is_alive():
    """Check if the API starts correctly"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_prediction():
    """Check if the model can actually predict"""
    payload = {
        "Close": 100.0,
        "SMA_10": 102.0,
        "SMA_50": 98.0,
        "Volatility": 2.5
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "predicted_price" in response.json()