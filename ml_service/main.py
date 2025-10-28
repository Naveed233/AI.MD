"""
FastAPI ML Microservice for Merchandising System
Handles prediction, health checks, and model reloading
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
import logging
from typing import List, Optional
from google.cloud import storage, logging as cloud_logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize GCP logging
try:
    client = cloud_logging.Client()
    client.setup_logging()
except Exception as e:
    logger.warning(f"Could not setup GCP logging: {e}")

app = FastAPI(title="MD ML Service", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
MODEL_PATH = "/app/models/model.pkl"
GCS_BUCKET = os.getenv("GCS_BUCKET", "md-system-data")
PROJECT_ID = os.getenv("PROJECT_ID")

# Global model variable
model = None
storage_client = None

# Request/Response models
class PredictionRequest(BaseModel):
    customer_id: str
    age: float
    purchase_history: int
    avg_order_value: float
    last_purchase_days: int
    region: str
    seasonality_factor: float = 1.0

class PredictionResponse(BaseModel):
    predicted_demand: float
    category: str
    optimal_stock: int
    confidence: float

class ReloadResponse(BaseModel):
    status: str
    message: str

def load_model_from_gcs():
    """Load model from Google Cloud Storage"""
    global model, storage_client
    
    try:
        if not storage_client:
            storage_client = storage.Client(project=PROJECT_ID)
        
        bucket = storage_client.bucket(GCS_BUCKET)
        blob = bucket.blob("models/model.pkl")
        
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        
        blob.download_to_filename(MODEL_PATH)
        model = joblib.load(MODEL_PATH)
        logger.info("Model loaded successfully from GCS")
        return model
    except Exception as e:
        logger.error(f"Failed to load model from GCS: {e}")
        # Try loading local model as fallback
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            logger.info("Loaded model from local filesystem")
            return model
        raise

def load_model_local():
    """Load model from local filesystem"""
    global model
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            logger.info("Model loaded from local filesystem")
        else:
            logger.warning("No local model found. Using dummy model.")
            # Create a dummy model for development
            from sklearn.ensemble import RandomForestRegressor
            model = RandomForestRegressor()
        return model
    except Exception as e:
        logger.error(f"Failed to load local model: {e}")
        raise

@app.on_event("startup")
async def startup_event():
    """Initialize model on startup"""
    global model
    try:
        if GCS_BUCKET and os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            model = load_model_from_gcs()
        else:
            model = load_model_local()
    except Exception as e:
        logger.error(f"Startup error: {e}")
        model = load_model_local()

@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "bucket": GCS_BUCKET
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Predict merchandising demand based on customer features
    """
    global model
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Prepare features
        features = {
            'age': request.age,
            'purchase_history': request.purchase_history,
            'avg_order_value': request.avg_order_value,
            'last_purchase_days': request.last_purchase_days,
            'seasonality_factor': request.seasonality_factor,
            'region_encoded': hash(request.region) % 10  # Simple encoding
        }
        
        df = pd.DataFrame([features])
        
        # Predict
        predicted_demand = model.predict(df)[0]
        
        # Additional predictions
        category = "High" if predicted_demand > 100 else "Medium" if predicted_demand > 50 else "Low"
        optimal_stock = int(predicted_demand * 1.2)  # 20% buffer
        confidence = min(0.95, 0.7 + (predicted_demand / 200))
        
        logger.info(f"Prediction for customer {request.customer_id}: {predicted_demand}")
        
        return PredictionResponse(
            predicted_demand=float(predicted_demand),
            category=category,
            optimal_stock=optimal_stock,
            confidence=float(confidence)
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reload", response_model=ReloadResponse)
async def reload_model():
    """
    Reload the latest model from GCS
    """
    global model
    
    try:
        if GCS_BUCKET and os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            model = load_model_from_gcs()
            return ReloadResponse(
                status="success",
                message="Model reloaded from GCS"
            )
        else:
            model = load_model_local()
            return ReloadResponse(
                status="success",
                message="Model reloaded from local filesystem"
            )
    except Exception as e:
        logger.error(f"Reload error: {e}")
        return ReloadResponse(
            status="error",
            message=str(e)
        )

@app.get("/")
async def root():
    return {
        "service": "MD ML Service",
        "version": "1.0.0",
        "endpoints": ["/health", "/predict", "/reload"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

