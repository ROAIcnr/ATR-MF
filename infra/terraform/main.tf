terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    bucket = "aetherium-terraform-state"
    prefix = "env/dev"
  }
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}
