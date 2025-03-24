terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.16.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}


resource "google_storage_bucket" "edgar-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = false
  uniform_bucket_level_access = true  
  storage_class = "REGIONAL"  
}

resource "google_bigquery_dataset" "edgar_dataset" {
  dataset_id = var.bq_dataset_name
  location = var.location
}
