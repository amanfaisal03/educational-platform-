import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(override=True)

class Settings(BaseSettings):
    database_url: str
    # front_end_url: str
    secret_key: str = "0c4bf72e725e337a63dc87f8efe350ff8b21c8e1b53cf2520533ef957fcd6acb"

    _project_root = Path(__file__).resolve().parent
    _env_file = _project_root / ".env"
    model_config = SettingsConfigDict(
        env_file=str(_env_file),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()

__all__ = ["Settings"]
