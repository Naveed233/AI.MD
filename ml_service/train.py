"""
Training script for Merchandising ML Model
Designed to run on Vertex AI as a CustomJob
"""

import pandas as pd
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from google.cloud import storage
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_synthetic_data(n_samples=1000):
    """Generate synthetic training data"""
    np.random.seed(42)
    
    data = {
        'age': np.random.normal(35, 10, n_samples),
        'purchase_history': np.random.poisson(20, n_samples),
        'avg_order_value': np.random.gamma(2, 50, n_samples),
        'last_purchase_days': np.random.exponential(30, n_samples),
        'seasonality_factor': np.random.uniform(0.5, 2.0, n_samples),
        'region_encoded': np.random.randint(0, 10, n_samples)
    }
    
    # Create target with some non-linearity
    data['target'] = (
        10 * data['purchase_history'] +
        2 * data['avg_order_value'] +
        5 * (data['seasonality_factor'] ** 2) +
        -0.1 * data['last_purchase_days'] +
        np.random.normal(0, 20, n_samples)
    )
    
    return pd.DataFrame(data)

def train_model():
    """Main training function"""
    
    # Configuration
    GCS_BUCKET = os.getenv("GCS_BUCKET", "md-system-data")
    PROJECT_ID = os.getenv("PROJECT_ID")
    
    logger.info(f"Starting model training for bucket: {GCS_BUCKET}")
    
    # Try to load data from GCS
    storage_client = None
    df = None
    
    try:
        if GCS_BUCKET and os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            storage_client = storage.Client(project=PROJECT_ID)
            bucket = storage_client.bucket(GCS_BUCKET)
            
            # Try to download training data
            blob = bucket.blob("training/data.csv")
            if blob.exists():
                blob.download_to_filename("data.csv")
                df = pd.read_csv("data.csv")
                logger.info("Loaded training data from GCS")
            else:
                logger.warning("No training data in GCS, generating synthetic data")
                df = generate_synthetic_data()
        else:
            logger.info("No GCS credentials, using synthetic data")
            df = generate_synthetic_data()
    
    except Exception as e:
        logger.warning(f"Could not load from GCS: {e}. Using synthetic data.")
        df = generate_synthetic_data()
    
    # Prepare features
    feature_columns = [col for col in df.columns if col != 'target']
    X = df[feature_columns]
    y = df['target']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    logger.info(f"Training on {len(X_train)} samples")
    
    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    logger.info(f"Model Performance:")
    logger.info(f"  MSE: {mse:.2f}")
    logger.info(f"  MAE: {mae:.2f}")
    logger.info(f"  R²: {r2:.2f}")
    
    # Save model locally
    os.makedirs("models", exist_ok=True)
    model_path = "models/model.pkl"
    joblib.dump(model, model_path)
    logger.info(f"Model saved to {model_path}")
    
    # Upload to GCS if available
    if storage_client:
        try:
            bucket = storage_client.bucket(GCS_BUCKET)
            blob = bucket.blob("models/model.pkl")
            blob.upload_from_filename(model_path)
            logger.info(f"Model uploaded to gs://{GCS_BUCKET}/models/model.pkl")
        except Exception as e:
            logger.error(f"Failed to upload to GCS: {e}")
    
    # Save training metrics
    metrics = {
        'mse': float(mse),
        'mae': float(mae),
        'r2': float(r2),
        'n_train': len(X_train),
        'n_test': len(X_test)
    }
    
    metrics_path = "models/metrics.json"
    import json
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f)
    
    if storage_client:
        try:
            bucket = storage_client.bucket(GCS_BUCKET)
            blob = bucket.blob("models/metrics.json")
            blob.upload_from_filename(metrics_path)
        except Exception as e:
            logger.error(f"Failed to upload metrics: {e}")
    
    logger.info("Training completed successfully")
    return model

if __name__ == "__main__":
    train_model()

