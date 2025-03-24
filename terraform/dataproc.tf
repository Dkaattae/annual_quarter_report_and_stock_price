resource "google_storage_bucket" "dataproc_staging" {
  name     = "edgar_dataproc-staging-bucket"
  location = "us-central1"

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 7
    }
  }
}

resource "google_dataproc_cluster" "dataproc_cluster" {
  name   = "edgar-dataproc-cluster"
  region = "us-central1"

  cluster_config {
    staging_bucket = google_storage_bucket.dataproc_staging.name

    master_config {
      num_instances = 1
      machine_type  = "n1-standard-4"
      disk_config {
        boot_disk_size_gb = 50
      }
    }

    worker_config {
      num_instances = 2
      machine_type  = "n1-standard-4"
      disk_config {
        boot_disk_size_gb = 50
      }
    }

    software_config {
      image_version = "2.1-debian10"
      optional_components = ["JUPYTER"]  # Optional components like Jupyter
    }

    initialization_action {
      script = "gs://your-gcs-bucket/init-script.sh"
    }
  }
}