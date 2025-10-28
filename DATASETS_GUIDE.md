# 📊 Free Datasets for AI Merchandising System

This guide lists the best free datasets you can use for training your ML model.

## 🌟 Top Recommended Datasets

### 1. **UCI Online Retail Dataset** (BEST CHOICE)
- **URL**: https://archive.ics.uci.edu/ml/datasets/Online+Retail
- **Size**: 541,910 transactions
- **Source**: UK-based online retailer
- **Fields**: 
  - InvoiceNo, StockCode, Description, Quantity
  - InvoiceDate, UnitPrice, CustomerID, Country
- **Why it's great**: Real transaction data perfect for demand forecasting
- **Download**: Direct CSV file available on UCI website

### 2. **Kaggle Online Retail Dataset**
- **URL**: https://www.kaggle.com/datasets/carrie1/ecommerce-data
- **Alternative to UCI dataset** (same data, easier to download)
- Requires Kaggle account (free)
- Download via: `kaggle datasets download -d carrie1/ecommerce-data`

### 3. **Kaggle Store Item Demand Forecasting**
- **URL**: https://www.kaggle.com/datasets
- **Search for**: "store item demand forecasting challenge"
- **Perfect for**: Time-series demand prediction
- **Includes**: Sales data over time for multiple stores and items

### 4. **Kaggle Online Shopper Purchasing Intention**
- **URL**: https://www.kaggle.com/datasets
- **Search for**: "Online Shopper Purchasing Intention Dataset"
- **Includes**: Customer session data, duration, page values, exit rates
- **Good for**: Customer behavior prediction

## 🎯 How to Add Real Data to Your System

### Step 1: Download Dataset
```bash
# Example: Download UCI Online Retail dataset
curl -O https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx

# Or use Kaggle CLI:
kaggle datasets download -d carrie1/ecommerce-data
unzip ecommerce-data.zip
```

### Step 2: Preprocess Data
Your ML service expects data with these features:
- `age`: Customer age
- `purchase_history`: Number of past purchases
- `avg_order_value`: Average order value
- `last_purchase_days`: Days since last purchase
- `seasonality_factor`: Seasonal adjustment factor
- `region_encoded`: Region encoded as number

Create a preprocessing script:
```python
import pandas as pd

# Load UCI dataset
df = pd.read_excel('Online Retail.xlsx')

# Preprocess to match your schema
# Extract features from transaction data
# Save as CSV for training
df.to_csv('training_data.csv', index=False)
```

### Step 3: Train Model
```bash
cd ml_service
python train.py
```

### Step 4: Upload to GCS (Optional)
```bash
gsutil cp models/model.pkl gs://md-system-data/models/
```

## 📈 Quick Start with Synthetic Data

If you want to test immediately without downloading external data:

```bash
# The training script already generates synthetic data!
docker compose exec ml_service python train.py

# This creates a model based on realistic synthetic patterns
# Perfect for development and testing
```

## 🎓 Alternative Data Sources

### Academic Datasets:
- **Mendeley Data**: Search "retail sales" or "e-commerce"
- **Zenodo**: Open scientific datasets
- **Harvard Dataverse**: Research datasets

### Government Datasets:
- **Data.gov**: US government open data
  - Search for "retail trade" or "commerce"
- **UK Data Service**: UK retail statistics
- **Eurostat**: European retail data

### Synthetic Data Generators:
- **Faker** library (Python): Generate realistic fake data
  ```python
  from faker import Faker
  fake = Faker()
  ```

## 🔍 What Data Fields You Need

Your model currently expects:
```python
{
    "customer_id": str,
    "age": float,           # Customer age
    "purchase_history": int, # Number of purchases
    "avg_order_value": float,  # Average $ spent
    "last_purchase_days": int,  # Days since last purchase
    "region": str,          # Geographic region
    "seasonality_factor": float  # Seasonal adjustment
}
```

## 💡 Tips for Choosing Datasets

1. **Look for transaction-level data** - More granular = better predictions
2. **Check data quality** - Ensure minimal missing values
3. **Consider data size** - 10K+ records recommended
4. **Match your use case** - Retail/e-commerce data works best
5. **Check licensing** - Ensure commercial use is allowed

## 🚀 Ready to Use Right Now

Your system is already using synthetic data! To test with real data:

1. Choose a dataset from above
2. Download and preprocess it
3. Run training: `docker compose exec ml_service python train.py`
4. Test predictions at: http://localhost:8080/predict

The model will automatically improve with better data!

