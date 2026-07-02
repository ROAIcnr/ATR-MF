from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    project_name: str = "Aetherium Manifest"
    environment: str = "dev"

    # GCP infra
    gcp_project: str = "aetherium-dev"
    gcp_region: str = "asia-southeast1"

    # AetherBus / Redis / Kafka
    redis_url: str = "redis://redis:6379/0"
    kafka_brokers: str = "kafka:9092"

    # DB
    postgres_dsn: str = "postgresql+asyncpg://aether:aether@postgres:5432/aetherium"

    # Security
    jwt_secret: str = "CHANGE_ME"
    jwt_issuer: str = "aetherium"
    jwt_audience: str = "aetherium-clients"

    class Config:
        env_file = ".env"

settings = Settings()
