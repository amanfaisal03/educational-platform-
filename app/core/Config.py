from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    secure_cookies: bool = True
    admin_name: str
    admin_password: str
    admin_email: str

    _project_root = Path(__file__).resolve().parents[2]
    _env_file = _project_root / ".env"
    model_config = SettingsConfigDict(
        env_file=str(_env_file),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

settings = Settings()

__all__ = ["Settings"]
