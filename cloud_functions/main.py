"""
Cloud Function triggered when new training data is uploaded to GCS
Automatically triggers Vertex AI training job
"""

import os
import json
from google.cloud import aiplatform
from google.cloud import logging
import functions_framework

# Configure logging
logging_client = logging.Client()
logging_client.setup_logging()

@functions_framework.cloud_event
def retrain_on_upload(cloud_event):
    """
    Triggered when a new file is uploaded to gs://{bucket}/training/
    Starts a Vertex AI CustomJob to retrain the model
    """
    
    # Parse the event data
    data = cloud_event.get_data()
    bucket_name = data.get("bucket")
    file_name = data.get("name")
    
    print(f"File uploaded: gs://{bucket_name}/{file_name}")
    
    # Configuration
    PROJECT_ID = os.getenv("GCS_PROJECT_ID", os.getenv("GCP_PROJECT"))
    REGION = os.getenv("REGION", "asia-northeast1")
    
    if not PROJECT_ID:
        raise ValueError("GCS_PROJECT_ID or GCP_PROJECT must be set")
    
    # Initialize Vertex AI
    aiplatform.init(project=PROJECT_ID, location=REGION)
    
    # Get Artifact Registry image
    ARTIFACT_REGISTRY_REPO = os.getenv("ARTIFACT_REGISTRY_REPO", "md")
    IMAGE_URI = f"{REGION}-docker.pkg.dev/{PROJECT_ID}/{ARTIFACT_REGISTRY_REPO}/ml-train:latest"
    
    print(f"Triggering training job with image: {IMAGE_URI}")
    
    # Create CustomJob
    job = aiplatform.CustomJob(
        display_name="md-retraining-job",
        worker_pool_specs=[{
            "machine_spec": {
                "machine_type": "n1-standard-4"
            },
            "replica_count": 1,
            "container_spec": {
                "image_uri": IMAGE_URI,
                "env": [
                    {
                        "name": "GCS_BUCKET",
                        "value": bucket_name
                    },
                    {
                        "name": "PROJECT_ID",
                        "value": PROJECT_ID
                    }
                ]
            }
        }]
    )
    
    # Run the job
    print("Starting training job...")
    job.run(sync=False)  # Don't wait for completion
    
    print(f"Training job {job.name} started successfully")
    
    return {
        "status": "success",
        "job_name": job.name,
        "bucket": bucket_name,
        "file": file_name
    }

