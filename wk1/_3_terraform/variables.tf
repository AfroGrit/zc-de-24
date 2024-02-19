variable "cloud_project_id" {
  description = "GCP project"
  default     = "data eng project"
}

variable "cloud_region" {
  description = "The region for your GCP resources"
  type        = string
  default     = "data eng cloud region"
}

variable "cloud_bucket_name" {
  description = "The unique name for your Google Storage Bucket"
  default     = "data eng cloud bucket name"
}

variable "cloud_cluster_name" {
  description = "The unique name for your Google Storage Bucket"
  default     = "data eng cloud cluster name"
}

variable "cloud_dataset_id" {
  description = "The name for your BigQuery Dataset"
  default     = "data eng cloud dataset"
}

variable "cloud_credentials" {
  description = "The path to your service account key JSON file"
  default     = "cloud_credentials"
}


variable "cloud_bigquery" {
  description = "BigQuery Dataset (from GCS) will be written to"
  type        = string
  default     = "cloud bigquery"
}
