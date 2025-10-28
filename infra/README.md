# Infrastructure as Code

This directory contains infrastructure setup scripts for deploying the MD System to Google Cloud Platform.

## Prerequisites

- Google Cloud SDK installed and configured
- Authenticated with `gcloud auth login`
- Project billing enabled

## Setup

### 1. Set Environment Variables

```bash
export PROJECT_ID=your-project-id
export REGION=asia-northeast1
export GCS_BUCKET=md-system-data
```

### 2. Run Setup Script

```bash
chmod +x infra/gcp_setup.sh
./infra/gcp_setup.sh
```

This script will:
- Enable all required GCP APIs
- Create Artifact Registry repository
- Create Cloud Storage bucket
- Create Cloud SQL instance
- Set up Cloud Function for auto-retraining
- Configure IAM permissions

## Manual Setup

If you prefer to set up resources manually:

1. Enable APIs
2. Create Artifact Registry
3. Create Cloud Storage bucket
4. Create Cloud SQL instance
5. Deploy Cloud Function
6. Configure IAM roles

## Architecture

```
┌─────────────────┐
│   Cloud Run     │
│   (Frontend)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Cloud Run     │
│   (Backend)     │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────────┐
│ Cloud  │ │   Cloud Run      │
│  SQL   │ │   (ML Service)   │
└────────┘ └────────┬──────────┘
                   │
                   ▼
              ┌──────────┐
              │   GCS    │
              │  Bucket  │
              └────┬─────┘
                   │
                   ▼ (trigger)
              ┌──────────────────┐
              │  Cloud Function  │
              │  (Auto-retrain)  │
              └────────┬─────────┘
                       │
                       ▼
                 ┌─────────────────┐
                 │  Vertex AI      │
                 │  CustomJob      │
                 └─────────────────┘
```

## Monitoring

- Cloud Logging: View logs for all services
- Cloud Monitoring: Set up alerts for service health
- Vertex AI: Monitor model performance and predictions

## Cost Estimation

- Cloud Run: Pay per use (~$0.0000002 per request-second)
- Cloud SQL: ~$25/month for db-f1-micro
- Cloud Storage: ~$0.026 per GB per month
- Vertex AI: Pay per training job (~$1-5 per job)
- Cloud Build: ~$0.003 per build-minute

Total estimated cost: ~$50-100/month for light usage

