# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """All runtime configuration, validated at startup."""
    model_config = SettingsConfigDict(env_file=".env", env_prefix="CARDGUARD_")

    db_path: str = "cardguard.db"
    api_url: str = "http://127.0.0.1:8000"
    review_threshold: float = 0.55
    decline_threshold: float = 0.80
    velocity_window_minutes: int = 10
    log_level: str = "INFO"

settings = Settings()

