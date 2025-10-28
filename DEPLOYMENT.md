# Deployment Guide

Complete step-by-step guide for deploying the MD System to Google Cloud Platform.

## Prerequisites

1. **Google Cloud Account**
   - Active billing account
   - Sufficient quotas enabled

2. **Local Setup**
   - Google Cloud SDK installed
   - Docker installed
   - Authentication configured

## Step 1: Initial GCP Setup

```bash
# Login to GCP
gcloud auth login

# Set your project
export PROJECT_ID=your-project-id
export REGION=asia-northeast1

gcloud config set project $PROJECT_ID
```

## Step 2: Run Infrastructure Setup

```bash
chmod +x infra/gcp_setup.sh
./infra/gcp_setup.sh
```

This will:
- Enable all required APIs
- Create Artifact Registry
- Create Cloud Storage bucket
- Set up Cloud SQL
- Create Cloud Function
- Configure IAM permissions

## Step 3: Build Initial Model

Before deploying, you need to train an initial model:

```bash
# Navigate to ML service
cd ml_service

# Run training locally (or on Vertex AI)
python train.py

# Upload model to GCS
gsutil cp models/model.pkl gs://md-system-data/models/
```

## Step 4: Deploy Services

### Option A: Using Cloud Build (Recommended)

```bash
# From project root
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=REGION=$REGION,GCS_BUCKET=md-system-data
```

### Option B: Manual Deployment

#### 4.1 Deploy ML Service

```bash
cd ml_service

# Build and push image
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/md/ml-service

# Deploy to Cloud Run
gcloud run deploy ml-service \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/md/ml-service \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 540 \
  --set-env-vars GCS_BUCKET=md-system-data,PROJECT_ID=$PROJECT_ID
```

#### 4.2 Deploy Backend

```bash
cd ../backend

# Build and push
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/md/backend

# Deploy
gcloud run deploy backend \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/md/backend \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "ML_API_URL=https://ml-service-$(gcloud config get-value project).${REGION}.run.app"
```

#### 4.3 Deploy Frontend

```bash
cd ../frontend

# Build and push
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/md/frontend

# Deploy
gcloud run deploy frontend \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/md/frontend \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated
```

## Step 5: Configure Environment Variables

Update your Cloud Run services with proper environment variables:

```bash
# Get ML service URL
export ML_SERVICE_URL=$(gcloud run services describe ml-service --region $REGION --format='value(status.url)')

# Update backend
gcloud run services update backend \
  --region $REGION \
  --set-env-vars "ML_API_URL=$ML_SERVICE_URL"
```

## Step 6: Set Up Cloud Function for Auto-Retraining

```bash
cd cloud_functions

# Deploy the function
gcloud functions deploy retrain-on-upload \
  --gen2 \
  --runtime=python311 \
  --region=$REGION \
  --source=. \
  --entry-point=retrain_on_upload \
  --trigger-bucket=md-system-data \
  --trigger-path="training/**" \
  --set-env-vars="PROJECT_ID=$PROJECT_ID,REGION=$REGION,GCS_BUCKET=md-system-data" \
  --timeout=540s \
  --memory=512MB
```

## Step 7: Set Up Cloud SQL Connection

```bash
# Connect Cloud SQL to Cloud Run
gcloud sql instances patch md-sql-instance \
  --database-flags=cloudsql.enable_iam_login=on \
  --region=$REGION

# Get connection name
export CONNECTION_NAME=$(gcloud sql instances describe md-sql-instance --format='value(connectionName)')
```

## Step 8: Test Deployment

```bash
# Get service URLs
export FRONTEND_URL=$(gcloud run services describe frontend --region $REGION --format='value(status.url)')
export BACKEND_URL=$(gcloud run services describe backend --region $REGION --format='value(status.url)')
export ML_URL=$(gcloud run services describe ml-service --region $REGION --format='value(status.url)')

# Test ML service
curl $ML_URL/health

# Test backend
curl $BACKEND_URL/api/v1/health

# Test prediction
curl -X POST $BACKEND_URL/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "TEST001",
    "age": 35,
    "purchase_history": 20,
    "avg_order_value": 150.50,
    "last_purchase_days": 7,
    "region": "North America",
    "seasonality_factor": 1.2
  }'
```

## Step 9: Set Up Monitoring

1. **Enable Cloud Monitoring**

```bash
gcloud monitoring notification-channels create \
  --display-name="Alerts" \
  --type=email \
  --channel-labels=email_address=your-email@example.com
```

2. **Create Alert Policies**
   - Go to Cloud Console > Monitoring > Alerting
   - Create alerts for:
     - Service uptime < 99%
     - Response latency > 2s
     - Error rate > 1%

## Step 10: Set Up CI/CD

1. **Connect Repository to Cloud Build**

```bash
gcloud source repos create md-system
gcloud source repos clone md-system

# Add your code and push
cd md-system
git remote add origin https://source.developers.google.com/p/$PROJECT_ID/r/md-system
git push origin main
```

2. **Create Build Trigger**

```bash
gcloud builds triggers create cloud-source-repositories \
  --repo=md-system \
  --branch-pattern=".*" \
  --build-config=cloudbuild.yaml
```

## Troubleshooting

### Service Not Accessible

```bash
# Check service status
gcloud run services describe SERVICE_NAME --region $REGION

# Check logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=SERVICE_NAME" --limit 50
```

### Model Not Loading

```bash
# Check GCS permissions
gsutil iam ch serviceAccount:SERVICE_ACCOUNT@PROJECT.iam.gserviceaccount.com:objectViewer gs://md-system-data

# Verify model exists
gsutil ls gs://md-system-data/models/
```

### Cloud Function Not Triggering

```bash
# Check function logs
gcloud functions logs read retrain-on-upload --limit 50

# Test manual upload
gsutil cp test_data.csv gs://md-system-data/training/
```

## Cost Optimization

1. **Cloud Run**: Set min instances to 0 for cost savings
2. **Cloud SQL**: Use stop/resume for non-production
3. **Cloud Build**: Limit concurrent builds
4. **Vertex AI**: Use minimal machine types for training

## Security Best Practices

1. **Enable Authentication**
   ```bash
   gcloud run services update SERVICE_NAME --region $REGION --no-allow-unauthenticated
   ```

2. **Use Service Accounts**
   ```bash
   gcloud iam service-accounts create ml-service-account
   ```

3. **Set Up VPC Connector** for private Cloud SQL access

4. **Enable Audit Logging**

## Next Steps

- Set up custom domain
- Configure load balancing
- Set up A/B testing
- Implement model versioning
- Add monitoring dashboards

