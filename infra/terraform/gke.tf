resource "google_container_cluster" "aetherium_gke" {
  name     = "aetherium-gke"
  location = var.gcp_region

  autopilot {
    enabled = true
  }

  # Assuming network and subnetwork are defined or default
  # network    = google_compute_network.aetherium_vpc.self_link
  # subnetwork = google_compute_subnetwork.aetherium_subnet.self_link
}
