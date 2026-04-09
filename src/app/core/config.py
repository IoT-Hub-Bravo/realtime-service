import os


class Settings:
    KAFKA_BOOTSTRAP_SERVERS: str = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    KAFKA_GROUP_ID: str = os.environ.get("KAFKA_GROUP_ID", "realtime-service")
    KAFKA_TOPIC: str = os.environ.get("KAFKA_TOPIC", "telemetry.clean")

    JWT_SECRET: str = os.environ.get("JWT_SECRET", "change-me")
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", "HS256")
    JWT_ALLOWED_ROLES: set = {"admin", "client"}

    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", "8000"))


settings = Settings()
