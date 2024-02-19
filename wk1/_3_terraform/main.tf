# This Terraform configuration sets up a Google Cloud Platform (GCP) environment
# with a Google Storage Bucket and a BigQuery Dataset.

# Specify the required providers and their versions
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.16.0"
    }
  }
}

# Configure the Google Cloud provider
provider "google" {
  # Credentials only need to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS environment variable set
  credentials = file(var.cloud_credentials)
  project     = var.cloud_project_id
  region      = var.cloud_region
}

# Create a Google Storage Bucket for the data lake
resource "google_storage_bucket" "data-lake-bucket" {
  name     = var.cloud_bucket_name
  location = var.cloud_region

  # Recommended settings
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  # Enable versioning to keep all versions of an object in the bucket
  versioning {
    enabled = true
  }

  # Automatically delete objects after 30 days
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }

  # Allow force destroy of bucket when running 'terraform destroy'
  force_destroy = true
}

# Create a Google BigQuery Dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.cloud_dataset_id
  project    = var.cloud_project_id
  location   = var.cloud_region
}
