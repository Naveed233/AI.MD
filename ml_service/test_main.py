"""
Basic tests for ML Service
"""

import pytest
from fastapi.testclient import TestClient
from main import app
import os

@pytest.fixture
def client():
    return TestClient(app)

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data

def test_predict_endpoint(client):
    """Test prediction endpoint with sample data"""
    payload = {
        "customer_id": "TEST001",
        "age": 35.0,
        "purchase_history": 20,
        "avg_order_value": 150.50,
        "last_purchase_days": 7,
        "region": "North America",
        "seasonality_factor": 1.2
    }
    
    response = client.post("/predict", json=payload)
    
    # Should succeed if model is loaded (or 503 if not)
    assert response.status_code in [200, 503]
    
    if response.status_code == 200:
        data = response.json()
        assert "predicted_demand" in data
        assert "category" in data
        assert "optimal_stock" in data
        assert "confidence" in data

def test_predict_validation(client):
    """Test prediction endpoint with invalid data"""
    payload = {
        "customer_id": "",  # Empty ID should fail
        "age": -10  # Invalid age
    }
    
    response = client.post("/predict", json=payload)
    # FastAPI will return 422 for validation errors
    assert response.status_code in [422, 503]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

