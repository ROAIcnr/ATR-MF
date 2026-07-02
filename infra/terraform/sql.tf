resource "google_sql_database_instance" "aetherium" {
  name             = "aetherium-sql"
  database_version = "POSTGRES_15"
  region           = var.gcp_region

  settings {
    tier = "db-custom-2-4096"
    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
    }
  }
}
