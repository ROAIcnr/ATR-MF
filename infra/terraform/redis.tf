resource "google_redis_instance" "aetherium" {
  name           = "aetherium-redis"
  tier           = "STANDARD_HA"
  memory_size_gb = 4
  region         = var.gcp_region
}
