variable "credentials" {
  type        = string
  description = "My GCP credentials"
  sensitive   = true
  default     = "./keys/my-creds.json"
}

variable "project_id" {
  type        = string
  description = "My GCP project id"
  sensitive   = true
}

variable "region" {
  type        = string
  description = "MY GCP region"
}


variable "location" {
  type        = string
  description = "MY GCP location"
}

variable "bq_dataset_name" {
  description = "My BigQuery dataset name"
  default     = "dataset_demo"
}

variable "gcp_bucket_name" {
  description = "My storage bucket name"
  default     = "data-engineering-terra-bucket"
}

variable "gcp_storage_class" {
  description = "Bucket storage class"
  default     = "STANDARD"
}