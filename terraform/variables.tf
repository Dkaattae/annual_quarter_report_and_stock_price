variable "credentials" {
	description = "Path to Google Cloud credentials"
	type = string
}

variable "project" {
	description = "Project"
	default = "Edgar-data-pipeline"
}

variable "region" {
	description = "Region"
	default = "us-central1"
}

variable "location" {
	description = "Project Location"
	default = "us-central1"
}

variable "bq_dataset_name" {
	description = "My BigQuery Dataset Name"
	default = "edgar_data"
}

variable "gcs_bucket_name" {
	description = "My Storage Bucket Name"
	default = "edgar_company_submission_files"
}

variable "gcs_storage_class" {
	description = "Bucket Storage Class"
	default = "STANDARD"
}