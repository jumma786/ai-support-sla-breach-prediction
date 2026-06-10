"""Configuration management for the SLA breach prediction pipeline."""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Environment
    env: str = os.getenv("ENV", "development")
    debug: bool = env == "development"
    
    # Paths
    project_root: Path = Path(__file__).parent.parent
    data_dir: Path = project_root / "data"
    models_dir: Path = project_root / "models"
    logs_dir: Path = project_root / "logs"
    
    # Model Configuration
    model_name: str = "sla_breach_pipeline"
    model_version: str = "2.0.0"
    default_threshold: float = 0.50
    
    # Feature Configuration
    feature_set_version: str = "2.0.0"
    
    # API Configuration
    api_title: str = "SLA Breach Prediction API"
    api_version: str = "2.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # MLflow Configuration
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    mlflow_experiment_name: str = "sla-breach-prediction"
    
    # Data Validation
    min_records_for_validation: int = 100
    drift_detection_enabled: bool = True
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

# Create necessary directories
settings.data_dir.mkdir(parents=True, exist_ok=True)
settings.models_dir.mkdir(parents=True, exist_ok=True)
settings.logs_dir.mkdir(parents=True, exist_ok=True)
