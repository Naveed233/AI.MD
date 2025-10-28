#!/bin/bash
# GCP Infrastructure Setup Script
# Run this script to set up all required GCP resources

set -e

PROJECT_ID=${PROJECT_ID:-"your-project-id"}
REGION=${REGION:-"asia-northeast1"}
GCS_BUCKET=${GCS_BUCKET:-"md-system-data"}

echo "Setting up GCP infrastructure for MD System..."
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Bucket: $GCS_BUCKET"

# Enable APIs
echo "Enabling required APIs..."
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    cloudfunctions.googleapis.com \
    aiplatform.googleapis.com \
    storage-component.googleapis.com \
    sqladmin.googleapis.com \
    artifactregistry.googleapis.com \
    cloudresourcemanager.googleapis.com \
    --project=$PROJECT_ID

# Create Artifact Registry repository
echo "Creating Artifact Registry repository..."
gcloud artifacts repositories create md \
    --repository-format=docker \
    --location=$REGION \
    --project=$PROJECT_ID || echo "Repository already exists"

# Create Cloud Storage bucket
echo "Creating Cloud Storage bucket..."
gsutil mb -p $PROJECT_ID -l $REGION gs://$GCS_BUCKET || echo "Bucket already exists"

# Create folder structure in bucket
gsutil mkdir -p gs://$GCS_BUCKET/models/
gsutil mkdir -p gs://$GCS_BUCKET/training/

# Create Cloud SQL instance (optional - for production)
echo "Creating Cloud SQL instance..."
gcloud sql instances create md-sql-instance \
    --project=$PROJECT_ID \
    --database-version=MYSQL_8_0 \
    --tier=db-f1-micro \
    --region=$REGION || echo "Instance already exists"

# Create database
gcloud sql databases create md_system \
    --instance=md-sql-instance \
    --project=$PROJECT_ID || echo "Database already exists"

# Grant Cloud Functions permission to trigger Vertex AI
echo "Setting up service account permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${PROJECT_ID}@appspot.gserviceaccount.com" \
    --role="roles/aiplatform.admin"

# Grant Cloud Run service account permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${PROJECT_ID}@appspot.gserviceaccount.com" \
    --role="roles/storage.objectAdmin"

# Set up Cloud Function for auto-retraining
echo "Setting up Cloud Function..."
cd cloud_functions

# Deploy Cloud Function
gcloud functions deploy retrain_on_upload \
    --gen2 \
    --runtime=python311 \
    --region=$REGION \
    --source=. \
    --entry-point=retrain_on_upload \
    --trigger-bucket=$GCS_BUCKET \
    --trigger-path="training/**" \
    --set-env-vars="PROJECT_ID=$PROJECT_ID,REGION=$REGION,GCS_BUCKET=$GCS_BUCKET" \
    --timeout=540s \
    --memory=512MB \
    --project=$PROJECT_ID || echo "Function already exists"

cd ..

# Create service account for ML training
echo "Creating service account for ML training..."
gcloud iam service-accounts create ml-training-sa \
    --display-name="ML Training Service Account" \
    --project=$PROJECT_ID || echo "Service account already exists"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:ml-training-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/aiplatform.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:ml-training-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/storage.objectAdmin"

echo "Infrastructure setup complete!"
echo ""
echo "Next steps:"
echo "1. Run 'make build' to build all Docker images"
echo "2. Run 'make deploy' to deploy to GCP via Cloud Build"
echo "3. Or run 'make up' for local development"

